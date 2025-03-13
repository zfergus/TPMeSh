import numpy as np
import igl


def components(V: np.ndarray, F: np.ndarray):
    return igl.vertex_components_from_adjacency_matrix(igl.adjacency_matrix(F))[0]


def remove_small_components(V, F):
    C = components(V, F)
    component_size = {k: 0 for k in np.unique(C)}
    for c in C:
        component_size[c] += 1
    if len(component_size) > 1:
        print("Multiple components detected")
        largest_component = max(component_size, key=component_size.get)
        print(f"Keeping only the largest component {largest_component}")
        F = F[(C[F] == largest_component).all(axis=1)]
        V, F, *_ = igl.remove_unreferenced(V, F)
    return V, F


def is_single_surface(V: np.ndarray, F: np.ndarray):
    return len(np.unique(components(V, F))) == 1


def tet_volume(tet: np.ndarray):
    assert tet.shape == (4, 3)
    return np.linalg.det(np.hstack([np.ones((4, 1)), tet])) / 6


def lerp(a, b, t):
    assert 0 <= t <= 1
    return a + (b - a) * t


def scale_to_unit_cube(V: np.ndarray, domain: np.ndarray):
    return V / domain.max()


def scale_to_domain(V: np.ndarray, domain: np.ndarray):
    return V * domain.max()
