# import meshio
import numpy as np
import polyscope as ps
# import igl

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))  # noqa

from TPMeSh import ImplicitShell, SpatiallyVaryingTPMS
from TPMeSh.mesh_implicit import _mesh_implicit_surface

cube = ImplicitShell(SpatiallyVaryingTPMS(), 0.5)

print("Generating spatially varying tpms mesh...")
eps = 1e-14  # Add a small epsilon to the domain to avoid numerical clipping
domain = np.vstack([[0, 0, 0], cube.domain.reshape(1, 3)])
domain[0] -= eps
domain[1] += eps
domain -= np.ptp(domain, axis=0) / 2  # Center the domain
V, F, feature_edges = _mesh_implicit_surface(
    cube, elements_in_thickness=3, feature_edge_res=100,
    return_feature_edges=True, verbose=True)
# print(f"#V: {len(V)}, #T: {len(T)}")

# F, *_ = igl.boundary_facets(T)
# V, F, *_ = igl.remove_unreferenced(V, F)
# del T

# meshio.write(
#     "meshes/tpms_cube.ply",
#     # meshio.Mesh(V, {"tetra": T}),
#     meshio.Mesh(V, {"triangle": F}),
#     file_format="ply"
# )

ps.init()

ps_mesh = ps.register_surface_mesh("cube", V, F)
# ps_mesh = ps.register_volume_mesh("cube", V, T)

if feature_edges is not None:
    feature_vertices = np.vstack(feature_edges)
    feature_edges = np.arange(len(feature_vertices)).reshape(-1, 2)
    ps_net = ps.register_curve_network(
        "feature edges", feature_vertices, feature_edges, enabled=True)
    ps_net.add_scalar_quantity(
        "implicit",
        cube(
            feature_vertices[:, 0], feature_vertices[:, 1], feature_vertices[:, 2]),
        enabled=False)

ps.show()
