# https://github.com/pybind/pybind11/issues/1004
from _tpms import (
    schoen_gyroid,
    double_schoen_gyroid,
    schwarz_diamond,
    double_swartz_diamond,
    schwarz_primitive,
    double_schwarz_primitive,
    schoen_iwp,
    lipnoid,
    neovius,
    fischer_koch_s,
    schoen_frd,
    PMY,
    tubular_G_AB,
    tubular_G_C,
    BCC,

    schoen_gyroid_gradient,
    schwarz_diamond_gradient,
    schwarz_primitive_gradient,
    schoen_iwp_gradient,
    neovius_gradient,
    fischer_koch_s_gradient,
    schoen_frd_gradient,
    PMY_gradient,

    Implicit,
    ImplicitShell,
    InterpolatedTPMS,
    SpatiallyVaryingTPMS,
    FourierTPMS,
)

# from .main import ()

tpms = InterpolatedTPMS.TPMSs
