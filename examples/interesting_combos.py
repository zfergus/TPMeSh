import pathlib
import meshio
import numpy as np
import polyscope as ps
import igl

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))  # noqa

from TPMeSh.mesh_implicit import mesh_implicit
from TPMeSh.mesh_implicit_surface import mesh_implicit_surface
from TPMeSh import ImplicitShell, InterpolatedTPMS


def combo_to_name(x):
    return "_".join(map("{:.3f}".format, x))


np.random.seed(69)

interesting_combos = np.array([
    [0.4, 0, 0.6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.4, 0, 0, 0.4, 0.2],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
params = np.random.rand(3)
params /= params.sum()
params[[0, 1]] = np.round(params[[0, 1]], 2)
params[2] = 1 - params[:2].sum()
interesting_combos[
    -1, np.random.choice(np.arange(8), size=3, replace=False)] = params

ps.init()

for i, combo in enumerate(interesting_combos):
    tpms = ImplicitShell(InterpolatedTPMS(combo), 0.5)

    name = combo_to_name(combo)

    if pathlib.Path(f"meshes/{name}.ply").exists():
        print(f"Loading {name} mesh...")
        mesh = meshio.read(f"meshes/{name}.ply")
        V = mesh.points
        F = mesh.cells_dict["triangle"]
    else:
        print(f"Generating {name} mesh...")

        # eps = 1e-14  # Add a small epsilon to the domain to numericals clipping
        # domain = np.vstack([[0, 0, 0], tpms.domain.reshape(1, 3)])
        # domain[0] -= eps
        # domain[1] += eps
        # domain -= domain.ptp(axis=0) / 2  # Center the domain
        # V, F = mesh_implicit_surface(tpms, domain, res_y=200)

        V, T = mesh_implicit(
            tpms, elements_in_thickness=4, perturb=False, exude=False, verbose=True)
        print(f"#V: {len(V)}, #T: {len(T)}")

        F, *_ = igl.boundary_facets(T)
        V, F, *_ = igl.remove_unreferenced(V, F)
        del T

        meshio.write(
            f"meshes/{name}.ply",
            meshio.Mesh(V, {"triangle": F}),
            file_format="ply",
            binary=True
        )

    ps_mesh = ps.register_surface_mesh(str(i), V, F)

ps.show()
