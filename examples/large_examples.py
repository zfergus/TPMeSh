import meshio
# import trimesh
# import trimesh.creation
import igl
import numpy as np
import polyscope as ps

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))  # noqa

from TPMeSh import ImplicitShell, InterpolatedTPMS
from TPMeSh.mesh_implicit_surface import mesh_implicit_surface
from TPMeSh.mesh_implicit_periodic import tile_mesh


def param_to_name(param):
    return "_".join([f"{p:.3f}" for p in param])


params = np.array([
    [0.029, 0.066, 0.018, 0.270, 0.014, 0.000, 0.233, 0.370],
    [0.180, 0.035, 0.065, 0.210, 0.003, 0.001, 0.470, 0.036],
    [0.025, 0.396, 0.006, 0.218, 0.015, 0.014, 0.187, 0.139],
])

tilings = np.array([
    [16, 16, 2],
    [16, 16, 2],
    [8, 32, 2],
])

for param, tiling in zip(params, tilings):
    domain = np.array([[0, 0, 0], tiling * np.full(3, 2 * np.pi)])
    V, BF = mesh_implicit_surface(
        ImplicitShell(InterpolatedTPMS(param), thickness=0.5),
        domain, res_y=int(tiling[1]//16*800), intersect_with_box=True)
    print(f"|V|={len(V)} |BF|={len(BF)}")

    # Plot mesh
    # ps.init()
    # ps.register_surface_mesh("mesh", V, BF)
    # ps.show()
    # exit()

    # Scale V from [0, 2π] to [0, 50]
    V *= 50 / (2 * np.pi)
    # print(f"|V|={len(V)} |T|={len(T)}")

    # Tile the mesh
    # print("\nTiling:", tiling)
    # V, T = tile_mesh(V, T, domain=np.full(3, 50), repeats=(tiling + 2))
    # print(f"|V|={len(V)} |T|={len(T)}")

    # BF, *_ = igl.boundary_facets(T)
    # print(f"|BF|={len(BF)}")

    # Clip the mesh so it has flat sides
    # print("\nClipping")
    # box = trimesh.creation.box(bounds=[50 * np.ones(3), 50 * (tiling + 1)])
    # mesh = trimesh.Trimesh(vertices=V, faces=BF)
    # mesh = trimesh.boolean.intersection([mesh, box])
    # V = mesh.vertices - 50  # Place origin at (0, 0, 0)
    # BF = mesh.faces
    # print(f"|V|={len(V)} |BF|={len(BF)}")

    meshio.write(
        f"meshes/{param_to_name(param)} ({{}}x{{}}x{{}}).ply".format(*tiling),
        meshio.Mesh(V, {"triangle": BF}))

    # Plot mesh
    # ps.init()
    # ps.register_surface_mesh("mesh", V, BF)
    # ps.show()
