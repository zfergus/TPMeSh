import numpy as np
import polyscope as ps


def visualize_periodic_mesh(
        V: np.ndarray,
        F: np.ndarray,
        dx=None,
        deform_grad=None,
        scalar_quantities=None
):
    """Plot a periodic mesh (V, F) with an optional displacement grad."""
    dim = V.shape[1]

    register_mesh = ps.register_surface_mesh if F.shape[1] == 3 else ps.register_volume_mesh

    # Plot center cell with wireframe
    ps.init()
    if dim == 2:
        ps.set_navigation_style("planar")

    cell = register_mesh("cell", V, F)

    if scalar_quantities is not None:
        for name, value in scalar_quantities.items():
            cell.add_scalar_quantity(
                name, value, defined_on='vertices', cmap='viridis')

    # dx/dx̄ = d/dx̄ (x̄ + u) = I + du/dx̄
    if deform_grad is None:
        deform_grad = np.eye(dim)
    assert deform_grad.shape == (dim, dim)

    if dx is None:
        dx = V.max(axis=0) - V.min(axis=0)

    tiling_V = []
    tiling_F = []
    n = 0
    for i in dx[0] * np.arange(2):
        for j in dx[1] * np.arange(2):
            for k in ([0] if dim == 2 else -dx[2] * np.arange(2)):
                if i == 0 and j == 0 and k == 0:
                    continue  # Skip center cell

                offset = np.array([i, j, k])[:dim].reshape(-1, 1)
                offset = (deform_grad @ offset).flatten()

                tiling_V.extend(V + offset)
                tiling_F.extend(F + n)
                n = len(tiling_V)
    tiling_V = np.array(tiling_V)
    tiling_F = np.array(tiling_F)

    register_mesh(f"periodic tiling", tiling_V, tiling_F)

    ps.show()

    return tiling_V, tiling_F


def visualize_mesh(
        V: np.ndarray,
        F: np.ndarray,
        cell_scalar_quantities=None,
        feature_edges=None,
        feature_edge_scalar_quantity=None
):
    ps.init()

    if F.shape[1] == 3:
        mesh = ps.register_surface_mesh("mesh", V, F)
    else:
        mesh = ps.register_volume_mesh("mesh", V, F)

    if cell_scalar_quantities is not None:
        for name, value in cell_scalar_quantities.items():
            mesh.add_scalar_quantity(name, value, defined_on='cells')

    if feature_edges is not None:
        feature_vertices = np.vstack(feature_edges)
        feature_edges = np.arange(len(feature_vertices)).reshape(-1, 2)
        curves = ps.register_curve_network(
            "feature edges", feature_vertices, feature_edges, enabled=True)
        if feature_edge_scalar_quantity is not None:
            for name, value in feature_edge_scalar_quantity.items():
                curves.add_scalar_quantity(name, value, enabled=False)

    ps.show()
