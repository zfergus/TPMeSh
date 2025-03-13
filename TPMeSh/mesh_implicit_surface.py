import numpy as np


class Cuboid:
    def __init__(self, x0, x1):
        self.x0 = x0
        self.x1 = x1

    def __call__(self, X, Y, Z):
        return np.max([
            (X - self.x0[0]) * (X - self.x1[0]),
            (Y - self.x0[1]) * (Y - self.x1[1]),
            (Z - self.x0[2]) * (Z - self.x1[2])
        ], axis=0)


class Intersection:
    def __init__(self, domains):
        self.domains = domains

    def __call__(self, X, Y, Z):
        return np.max([domain(X, Y, Z) for domain in self.domains], axis=0)


def res3D(domain, res_y):
    x, y, z = np.hsplit(domain, 3)
    res_x = res_y * (x[1] - x[0]) / (y[1] - y[0])
    res_z = res_y * (z[1] - z[0]) / (y[1] - y[0])
    return int(res_x), int(res_y), int(res_z)


def _eval_implicit(f, domain, res_y):
    x, y, z = np.hsplit(domain, 3)

    res_x, res_y, res_z = res3D(domain, res_y)

    X, Y, Z = np.mgrid[0:res_x+1, 0:res_y+1, 0:res_z+1]
    X = x[0] + (x[1] - x[0]) * X / res_x
    Y = y[0] + (y[1] - y[0]) * Y / res_y
    Z = z[0] + (z[1] - z[0]) * Z / res_z

    return f(X.flatten(), Y.flatten(), Z.flatten()).reshape((res_x+1, res_y+1, res_z+1))


def mesh_implicit_surface(f, domain, res_y=100, intersect_with_box=False):
    import mcubes  # marching cubes

    # Add a small epsilon to the domain to avoid numerical clipping
    eps = np.ptp(domain) * 1e-6

    S = _eval_implicit(
        Intersection([f, Cuboid(domain[0]+eps, domain[1]-eps)]
                     ) if intersect_with_box else f,
        domain, res_y)
    print(S.min(), S.max())
    assert S.min() < 0 and S.max() > 0

    V, F = mcubes.marching_cubes(S, 0)
    assert len(V) > 0
    assert len(F) > 0

    F = F.astype(np.int64)

    # Scale to [0, 1]
    V = (V - V.min(axis=0)) / (V.max(axis=0) - V.min(axis=0))
    # Scale to domain
    V = (domain[1] - domain[0]) * V + domain[0]

    if np.isnan(V).any():
        raise ValueError("NaNs in mesh")

    return V, F
