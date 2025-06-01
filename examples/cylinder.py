import meshio
import numpy as np
import polyscope as ps

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))  # noqa

from TPMeSh import Implicit
from TPMeSh.mesh_implicit import mesh_implicit

r = 56.1 / 2
h = 153.9

cylinder = Implicit(
    f=lambda x, y, z: (x - r)**2 + (z - r)**2 - r**2,
    df=lambda x, y, z: np.array([2*(x - r), np.zeros_like(y), 2*(z - r)]),
    domain=np.array([2 * r, h, 2 * r])
)

print("Generating cylinder mesh...")
V, T, feature_edges = mesh_implicit(
    cylinder, elements_in_thickness=40, feature_edge_res=25, odt=True,
    return_feature_edges=True, verbose=True)
print(f"#V: {len(V)}, #T: {len(T)}")

meshio.write(
    "meshes/cylinder.msh",
    meshio.Mesh(V, {"tetra": T}),
    file_format="gmsh"
)

ps.init()

ps_mesh = ps.register_volume_mesh("cylinder", V, T)

if feature_edges is not None:
    feature_vertices = np.vstack(feature_edges)
    feature_edges = np.arange(len(feature_vertices)).reshape(-1, 2)
    ps_net = ps.register_curve_network(
        "feature edges", feature_vertices, feature_edges, enabled=True)
    ps_net.add_scalar_quantity(
        "implicit",
        cylinder(
            feature_vertices[:, 0], feature_vertices[:, 1], feature_vertices[:, 2]),
        enabled=False)

ps.show()
