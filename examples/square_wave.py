import meshio
import numpy as np
import polyscope as ps
import igl

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))  # noqa

from TPMeSh.mesh_implicit import mesh_implicit
from TPMeSh.mesh_implicit_surface import mesh_implicit_surface
from TPMeSh import ImplicitShell, FourierTPMS


tpms = ImplicitShell(FourierTPMS(), 0.5)

print(f"Generating mesh...")

# eps = 1e-14  # Add a small epsilon to the domain to avoid numerical clipping
# domain = np.vstack([[0, 0, 0], tpms.domain.reshape(1, 3)])
# domain[0] -= eps
# domain[1] += eps
# domain -= domain.ptp(axis=0) / 2  # Center the domain
# V, F = mesh_implicit_surface(tpms, domain, res_y=200)
# print(V.ptp(axis=0))

V, T = mesh_implicit(
    tpms, elements_in_thickness=4, perturb=False, exude=False, verbose=True)
print(f"#V: {len(V)}, #T: {len(T)}")

F, *_ = igl.boundary_facets(T)
V, F, *_ = igl.remove_unreferenced(V, F)
del T

meshio.write(
    f"meshes/square_wave.ply",
    meshio.Mesh(V, {"triangle": F}),
    file_format="ply",
    binary=True
)

ps.init()
ps_mesh = ps.register_surface_mesh("Square Wave", V, F)
ps.show()
