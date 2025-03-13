import numpy as np
import igl  # type: ignore
import pygalmesh  # type: ignore


class PyGalImplicit(pygalmesh.DomainBase):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def eval(self, X):
        assert (len(X) == 3)
        return self.f(*(self.f.domain * X))


def mesh_implicit_periodic(
        f,
        elements_in_thickness=2,
        perturb=True,
        exude=True,
        odt=False,
        lloyd=False,
        verbose=False):
    """
    Generate a periodic mesh of an implicit function using pygalmesh.

    Parameters:
    - f: implicit function
    - elements_in_thickness: number of elements in the thickness
    - verbose: print verbose output

    Returns:
    - V: vertices of the mesh
    - T: tetrahedra of the mesh
    - boundary_faces: boundary faces of the mesh
    """

    if hasattr(f, "thickness"):
        res = f.thickness / elements_in_thickness / f.domain.max()
    else:
        res = 0.025

    mesh = pygalmesh.generate_periodic_mesh(
        PyGalImplicit(f),
        [0, 0, 0, 1, 1, 1],  # unit cube
        manifold=True,
        max_cell_circumradius=res,
        max_radius_surface_delaunay_ball=res,
        max_facet_distance=min(0.1 * res, 0.000625),
        number_of_copies_in_output=1,
        perturb=perturb,
        exude=exude,
        odt=odt,
        lloyd=lloyd,
        verbose=verbose,
    )

    V = mesh.points.copy()  # Vertices of the mesh
    T = mesh.cells_dict["tetra"].copy()  # Tetrahedra of the mesh
    # Boundary surface of the cell
    boundary_faces = mesh.cells_dict["triangle"].copy()

    assert V.size > 0

    V, T, I, J = igl.remove_unreferenced(V, T)

    # The boundary_faces contains extra faces from accross the periodic boundary.
    # Filter these out by checking if the vertices are in the new vertex indices.
    boundary_faces = I[boundary_faces]
    boundary_faces = boundary_faces[np.all(boundary_faces >= 0, axis=1)]

    # Use the faces of T to determine the boundary faces with correct orientation
    mixed_faces, *_ = igl.boundary_facets(T)
    clean_boundary_faces = []
    for face in mixed_faces:
        if np.isin(face, boundary_faces).all():
            clean_boundary_faces.append(face)
    boundary_faces = np.array(clean_boundary_faces)

    # Determine which vertices are on the periodic boundary
    # mixed_faces, *_ = igl.boundary_facets(T)
    # interal_faces = mixed_faces[np.logical_not(
    #     np.isin(mixed_faces, boundary_faces).all(axis=1))]
    # periodic_vertices = np.unique(interal_faces)

    V *= f.domain  # Scale to domain

    return V, T, boundary_faces


def tile_mesh(V, T, domain, repeats):
    """Tile a mesh in 3D."""
    nV = len(V)

    for i, repeat in enumerate(repeats):
        offset = np.zeros(3)
        offset[i] = domain[i]
        V = np.vstack([
            V + r * offset for r in range(repeat)
        ])
    T = np.vstack([
        T + r * nV for r in range(np.prod(repeats))
    ])

    V, *_, T = igl.remove_duplicate_vertices(V, T, 1e-2)

    return V, T


def periodic_components(V, F, bounds=None):
    A = igl.adjacency_matrix(F).tolil()

    # Add periodic adjacencies
    if bounds is None:
        bounds = V.min(axis=0), V.max(axis=0)
    for i in range(3):
        for vi, v in enumerate(V):
            periodic_copy = v.copy()
            periodic_copy[i] += bounds[1][i] - bounds[0][i]

            vj = np.argmin(np.linalg.norm(V - periodic_copy, axis=1))

            if np.linalg.norm(V[vj] - periodic_copy) < 1e-10:
                A[vi, vj] = A[vj, vi] = 1

    return igl.vertex_components_from_adjacency_matrix(A.tocsc())[0]
