import numpy as np
import igl
import pygalmesh

from .mesh_implicit_surface import res3D
from .utils import remove_small_components, tet_volume, scale_to_unit_cube, scale_to_domain, lerp


CUBE_VERTICES = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
])
CUBE_EDGES = np.array([
    [0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
    [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]
])


class Intersection(pygalmesh.DomainBase):
    """Re-implement this in Python because the C++ version has a wrong get_features() implementation."""

    def __init__(self, domains):
        pygalmesh.DomainBase.__init__(self)
        self.domains = domains

    def eval(self, x):
        return max(domain.eval(x) for domain in self.domains)

    def get_bounding_sphere_squared_radius(self):
        return min(domain.get_bounding_sphere_squared_radius() for domain in self.domains)

    def get_features(self):
        # NOTE: Hardcoded to return the features of the first domain
        return self.domains[0].get_features()


class PyGALImplicit(pygalmesh.DomainBase):
    def __init__(self, f, repeats, feature_edge_res):
        from .mesh_implicit_surface import mesh_implicit_surface

        pygalmesh.DomainBase.__init__(self)
        self.f = f
        self.repeats = repeats

        eps = 1e-14  # Add a small epsilon to the domain to avoid numerical clipping
        domain = np.vstack([[0, 0, 0], (repeats * f.domain).reshape(1, 3)])
        domain[0] -= eps
        domain[1] += eps

        # Use mesh_implicit_surface to get the feature edges
        V, F = mesh_implicit_surface(f, domain=domain, res_y=feature_edge_res)

        # Scale vertices to unit cube for meshing
        ptp = np.ptp(V, axis=0)
        V = scale_to_unit_cube(V, repeats * f.domain)

        # Get boundary edges (i.e. open edges of the mesh)
        BE, *_ = igl.boundary_facets(F)

        # Add extra edges to capture the bbox edges
        extra_edges = []
        res = res3D(domain=domain, res_y=feature_edge_res)
        for a, b in (ptp * CUBE_VERTICES[CUBE_EDGES]):
            n = res[np.argmax(np.abs(b - a))]  # NOTE: edges are axis-aligned
            ts = np.linspace(0, 1, n + 1)
            for i in range(len(ts) - 1):
                c = lerp(a, b, ts[i])
                d = lerp(a, b, ts[i+1])

                sc = f(*c)
                sd = f(*d)

                if sc <= 0 or sd <= 0:
                    extra_edges.append([
                        c if sc <= 0 else lerp(c, d, sc / (sc - sd)),
                        d if sd <= 0 else lerp(c, d, sc / (sc - sd))
                    ])
        extra_edges = np.array(extra_edges)
        for edge in extra_edges:
            edge[:] = scale_to_unit_cube(edge, repeats * f.domain)

        # Combine feature edges and extra edges
        self.feature_edges = V[BE]
        if len(extra_edges) > 0:
            self.feature_edges = np.vstack([self.feature_edges, extra_edges])

    def eval(self, X):
        assert len(X) == 3
        return self.f(*scale_to_domain(np.array(X), self.repeats * self.f.domain))

    def get_bounding_sphere_squared_radius(self):
        raise RuntimeError("Not implemented")

    def get_features(self):
        return self.feature_edges.tolist()

    @property
    def min_edge_size_at_feature_edges(self):
        if len(self.feature_edges) == 0:
            return 0
        return np.linalg.norm(np.ptp(self.feature_edges, axis=1), axis=1).min()

    @property
    def max_edge_size_at_feature_edges(self):
        if len(self.feature_edges) == 0:
            return 0
        return np.linalg.norm(np.ptp(self.feature_edges, axis=1), axis=1).max()


def mesh_implicit(
    f,
    elements_in_thickness=2,
    feature_edge_res=100,
    repeats=np.ones(3),
    return_feature_edges=False,
    perturb=True,
    exude=None,
    odt=False,
    lloyd=False,
    verbose=False
):
    """
    Generate a mesh of an implicit function using pygalmesh.

    Parameters:
    - f: implicit function
    - elements_in_thickness: number of elements in the thickness of the mesh
    - feature_edge_res: resolution of the feature edges
    - repeats: number of repeats in each direction
    - return_feature_edges: return feature edges of the mesh
    - verbose: print debug information

    Returns:
    - V: vertices of the mesh
    - T: tetrahedra of the mesh
    - feature_edges: (if return_feature_edges is True) feature edges of the mesh
    """
    if exude is None:
        exude = elements_in_thickness > 1

    thickness = f.thickness if hasattr(f, "thickness") else f.domain.max()
    res = scale_to_unit_cube(
        thickness / elements_in_thickness, repeats * f.domain)
    if verbose:
        print("Mesh resolution:", res)

    implicit = PyGALImplicit(f, repeats, feature_edge_res=feature_edge_res)
    if verbose:
        print("Min/max edge size at feature edges:",
              implicit.min_edge_size_at_feature_edges,
              implicit.max_edge_size_at_feature_edges)

    # Normalize to unit cube
    bbox = np.array([
        [0, 0, 0], scale_to_unit_cube(repeats * f.domain, repeats * f.domain)
    ])
    if verbose:
        print("PyGAL bounding box:", bbox.tolist())

    mesh = pygalmesh.generate_mesh(
        Intersection([
            implicit,
            pygalmesh.Cuboid(*bbox)
        ]),
        bounding_cuboid=bbox.flatten(order="C"),
        max_cell_circumradius=res,
        max_radius_surface_delaunay_ball=res,
        max_facet_distance=0.1 * res,
        min_edge_size_at_feature_edges=res,
        odt=odt,
        lloyd=lloyd,
        perturb=perturb,
        exude=exude,
        verbose=verbose,
    )

    if verbose:
        print("Meshing done")

    V = mesh.points
    assert V.size > 0

    T = mesh.cells_dict["tetra"]
    assert T.size > 0

    volumes = np.array([tet_volume(tet) for tet in V[T]])
    if np.any(volumes < 1e-12):
        # Hopefully these elements are slivers with points close to each other
        nV = V.shape[0]
        V, *_, T = igl.remove_duplicate_vertices(V, T, 1e-12)
        print(f"Removed {nV - V.shape[0]:d} duplicate vertices!")
        volumes = np.array([tet_volume(tet) for tet in V[T]])
    T = T[volumes > 1e-12]

    V, T, *_ = igl.remove_unreferenced(V, T)

    assert all(tet_volume(tet) > 0 for tet in V[T])

    if verbose:
        print("Removing small components...")
    V, T = remove_small_components(V, T)

    # Translate to origin and scale to domain
    V = scale_to_domain(V - V.min(axis=0), repeats * f.domain)
    if verbose:
        print("Mesh bbox: ", V.min(axis=0), V.max(axis=0))

    # import ipctk
    # BF, *_ = ipctk.boundary_facets(T)
    # BE = ipctk.edges(BF)
    # collision_mesh = ipctk.CollisionMesh.build_from_full_mesh(V, BE, BF)
    # has_intersection = ipctk.has_intersections(
    #     collision_mesh, collision_mesh.rest_positions,
    #     broad_phase_method=ipctk.BroadPhaseMethod.BVH)
    # assert not has_intersection

    if return_feature_edges:
        if len(implicit.feature_edges) == 0:
            return V, T, None
        return V, T, repeats.max() * f.domain.max() * np.array(implicit.get_features())
    return V, T


def _mesh_implicit_surface(
    f,
    elements_in_thickness=2,
    feature_edge_res=100,
    repeats=np.ones(3),
    return_feature_edges=False,
    verbose=False
):
    """
    Generate a mesh of an implicit function using pygalmesh.

    Parameters:
    - f: implicit function
    - elements_in_thickness: number of elements in the thickness of the mesh
    - repeats: number of repeats in each direction
    - return_feature_edges: return feature edges of the mesh
    - verbose: print debug information

    Returns:
    - V: vertices of the mesh
    - F: triangles of the mesh
    - feature_edges: (if return_feature_edges is True) feature edges of the mesh
    """
    thickness = f.thickness if hasattr(f, "thickness") else f.domain.max()
    res = scale_to_unit_cube(
        thickness / elements_in_thickness, repeats * f.domain)
    if verbose:
        print("Mesh resolution:", res)

    implicit = PyGALImplicit(f, repeats, feature_edge_res=feature_edge_res)
    if verbose:
        print("Min/max edge size at feature edges:",
              implicit.min_edge_size_at_feature_edges,
              implicit.max_edge_size_at_feature_edges)

    # Normalize to unit cube
    bbox = np.array([
        [0, 0, 0], scale_to_unit_cube(repeats * f.domain, repeats * f.domain)
    ])
    bbox -= np.ptp(bbox, axis=0) / 2  # Center the bbox
    if verbose:
        print("PyGAL bounding box:", bbox.tolist())

    mesh = pygalmesh.generate_surface_mesh(
        Intersection([
            implicit,
            pygalmesh.Cuboid(*bbox)
        ]),
        bounding_sphere_radius=1.01 * np.linalg.norm(bbox[1]),
        max_radius_surface_delaunay_ball=res,
        max_facet_distance=0.1 * res,
        verbose=verbose,
    )

    if verbose:
        print("Meshing done")

    V = mesh.points
    assert V.size > 0

    F = mesh.cells_dict["triangle"]
    assert F.size > 0

    # if verbose:
    #     print("Removing small components...")
    # V, F = remove_small_components(V, F)

    # Translate to origin and scale to domain
    V = scale_to_domain(V - V.min(axis=0), repeats * f.domain)
    if verbose:
        print("Mesh bbox: ", V.min(axis=0), V.max(axis=0))

    if return_feature_edges:
        if len(implicit.feature_edges) == 0:
            return V, F, None
        return V, F, repeats.max() * f.domain.max() * np.array(implicit.get_features())
    return V, F
