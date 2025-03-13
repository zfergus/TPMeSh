import numpy as np
import igl

from _tpms import ImplicitShell, InterpolatedTPMS
from mesh_implicit_periodic import mesh_implicit_periodic
from mesh_implicit import mesh_implicit
from utils import is_single_surface, tet_volume
from visualize import visualize_mesh, visualize_periodic_mesh


def mesh_tpms_periodic(x, thickness, **kwargs):
    """Generate a periodic TPMS cell mesh with given design parameters."""
    return mesh_implicit_periodic(
        ImplicitShell(InterpolatedTPMS(x), thickness=thickness), **kwargs)


def mesh_tpms_full(x, thickness, **kwargs):
    """Generate a full TPMS mesh with given design parameters."""
    return mesh_implicit(
        ImplicitShell(InterpolatedTPMS(x), thickness=thickness), **kwargs)


def mesh_tpms_surface(x, thickness, **kwargs):
    """Generate a surface mesh from a TPMS volume mesh."""
    kwargs["perturb"] = False
    kwargs["exude"] = False

    if kwargs.get("periodic", False):
        results = mesh_tpms_periodic(x, thickness, **kwargs)
    else:
        results = mesh_tpms_full(x, thickness, **kwargs)
    V, T = results[:2]

    if kwargs.get("verbose", False):
        print("Extracting surface mesh...")
    F, *_ = igl.boundary_facets(T)
    V, F, *_ = igl.remove_unreferenced(V, F)
    F[:, [0, 1]] = F[:, [1, 0]]  # flip orientation

    if not is_single_surface(V, F):
        raise ValueError("Cavities detected")

    if len(results) > 2:
        return V, F, results[2]
    return V, F


def parse_args():
    import argparse
    import pathlib

    def parse_x(x):
        if x in ['r', "random"]:
            return np.random.rand(1)[0]
        return float(x)

    parser = argparse.ArgumentParser(
        description="Generate a TPMS mesh with given design parameters.")

    parser.add_argument("-x", nargs=8, type=parse_x, default=None,
                        help="design parameters")
    parser.add_argument("-i", type=int, default=None,
                        help="Generate a canonical TPMS with the given index")

    parser.add_argument(
        "-s", "--surface", action='store_true', help="generate surface mesh")
    parser.add_argument(
        "-p", "--periodic", action='store_true', help="generate periodic mesh")

    parser.add_argument(
        "-o", "--output", dest="output", type=pathlib.Path, default=None,
        help="output mesh name (.stl for surface mesh, .msh for volume mesh)")

    parser.add_argument(
        "-t", "--thickness", dest="thickness", type=float, default=0.5)
    parser.add_argument(
        "-n", "--elements-in-thickness", type=int, default=2,
        help="Number of elements in the thickness of the mesh (default: 2)")
    parser.add_argument(
        "-r", "--repeats", type=int, nargs=3, default=None,
        help="Number of repeats in each direction (default: 4 2 4 for full mesh, 1 1 1 for periodic mesh)")

    parser.add_argument(
        "-v", "--visualize", action='store_true', help="visualize the mesh")

    args = parser.parse_args()

    if args.i is None and args.x is None:
        parser.error("Either -i or -x must be specified")
    if (args.i is not None) and (args.x is not None):
        parser.error("Both -i and -x cannot be specified")

    if args.i is not None:
        args.x = np.zeros(8)
        args.x[args.i] = 1
        del args.i
    args.x = np.array(args.x)

    if args.output and not args.surface:
        args.output = args.output.with_suffix(".msh")

    if args.repeats is None:
        args.repeats = [4, 2, 4] if args.surface else [1, 1, 1]
    args.repeats = np.array(args.repeats)

    return args


def main():
    import meshio
    import polyscope as ps

    args = parse_args()

    print("Generating TPMS mesh...")
    if args.surface:
        V, F, feature_edges = mesh_tpms_surface(
            args.x, thickness=args.thickness, repeats=args.repeats, verbose=True,
            elements_in_thickness=args.elements_in_thickness, return_feature_edges=True)
    elif args.periodic:
        # TODO: repeats=args.repeats
        V, F, _ = mesh_tpms_periodic(
            args.x, thickness=args.thickness,
            elements_in_thickness=args.elements_in_thickness, verbose=True)
        feature_edges = []
    else:
        V, F, feature_edges = mesh_tpms_full(
            args.x, thickness=args.thickness, repeats=args.repeats, verbose=True,
            elements_in_thickness=args.elements_in_thickness, return_feature_edges=True)
    print(f"#V: {len(V)}, #F: {len(F)}")

    if not args.periodic:
        if len(feature_edges):
            feature_edges = 200 * (feature_edges - V.min(axis=0)) / np.ptp(V)
        V = 200 * (V - V.min(axis=0)) / np.ptp(V)

    # Save the mesh
    if args.output:
        mesh = meshio.Mesh(V, {"triangle" if args.surface else "tetra": F})
        if args.surface:
            meshio.write(args.output, mesh, binary=True)
        else:
            meshio.write(args.output, mesh, file_format="gmsh")
        print(f"Saved mesh to {args.output}")

    # Visualize the mesh
    if args.visualize:
        if args.periodic and not args.surface:
            domain = ImplicitShell(InterpolatedTPMS(
                args.x), thickness=args.thickness).domain
            visualize_periodic_mesh(V, F, dx=domain)
        else:
            if args.surface:
                scalar_values = None
            else:
                scalar_values = {
                    "volume": np.array([tet_volume(tet) for tet in V[F]])
                }
            if len(feature_edges):
                feature_vertices = np.vstack(feature_edges)
                feature_edge_scalar_quantity = {
                    "implicit": ImplicitShell(InterpolatedTPMS(args.x), thickness=args.thickness)(
                        feature_vertices[:, 0], feature_vertices[:, 1], feature_vertices[:, 2])
                }
            visualize_mesh(V, F, cell_scalar_quantities=scalar_values, feature_edges=feature_edges,
                           feature_edge_scalar_quantity=feature_edge_scalar_quantity)


if __name__ == "__main__":
    main()
