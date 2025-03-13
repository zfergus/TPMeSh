// https://nodtem66.github.io/Scaffolder/tutorial_2/#the-list-of-implicit-functions

#pragma once

#include <cmath>

namespace tpms {

/// @brief Domain of the TPMSs
static const Eigen::Array3d TPMS_DOMAIN = Eigen::Array3d::Constant(2 * M_PI);

inline double schoen_gyroid(const double x, const double y, const double z)
{
    return std::sin(x) * std::cos(y) + std::sin(y) * std::cos(z)
        + std::sin(z) * std::cos(x);
}

inline double
double_schoen_gyroid(const double x, const double y, const double z)
{
    return 2.75
        * (std::sin(2 * x) * std::sin(z) * std::cos(y)
           + std::sin(2 * y) * std::sin(x) * std::cos(z)
           + std::sin(2 * z) * std::sin(y) * std::cos(x))
        - (std::cos(2 * x) * std::cos(2 * y) + std::cos(2 * y) * std::cos(2 * z)
           + std::cos(2 * z) * std::cos(2 * x));
}

inline double schwarz_diamond(const double x, const double y, const double z)
{
    return std::cos(x) * std::cos(y) * std::cos(z)
        - std::sin(x) * std::sin(y) * std::sin(z);
}

inline double
double_swartz_diamond(const double x, const double y, const double z)
{
    return std::sin(2 * x) * std::sin(2 * y) + std::sin(2 * y) * std::sin(2 * z)
        + std::sin(2 * z) * std::sin(2 * x)
        + std::cos(2 * x) * std::cos(2 * y) * std::cos(2 * z);
}

inline double schwarz_primitive(const double x, const double y, const double z)
{
    return std::cos(x) + std::cos(y) + std::cos(z);
}

inline double
double_schwarz_primitive(const double x, const double y, const double z)
{
    return std::sin(x) * std::sin(y) * std::sin(z)
        + std::sin(x) * std::cos(y) * std::cos(z)
        + std::cos(x) * std::sin(y) * std::cos(z)
        + std::cos(x) * std::cos(y) * std::sin(z);
}

inline double schoen_iwp(const double x, const double y, const double z)
{
    return 2
        * (std::cos(x) * std::cos(y) + std::cos(y) * std::cos(z)
           + std::cos(z) * std::cos(x))
        - (std::cos(2 * x) + std::cos(2 * y) + std::cos(2 * z));
}

inline double lipnoid(const double x, const double y, const double z)
{
    return std::sin(2 * x) * std::cos(y) * std::sin(z)
        + std::sin(2 * y) * std::cos(z) * std::sin(x)
        + std::sin(2 * z) * std::cos(x) * std::sin(y)
        + std::cos(2 * x) * std::cos(2 * y) + std::cos(2 * y) * std::cos(2 * z)
        + std::cos(2 * z) * std::cos(2 * x);
}

inline double neovius(const double x, const double y, const double z)
{
    return 3 * (std::cos(x) + std::cos(y) + std::cos(z))
        + 4 * std::cos(x) * std::cos(y) * std::cos(z);
}

inline double fischer_koch_s(const double x, const double y, const double z)
{
    return std::cos(2 * x) * std::sin(y) * std::cos(z)
        + std::cos(x) * std::cos(2 * y) * std::sin(z)
        + std::sin(x) * std::cos(y) * std::cos(2 * z);
}

inline double schoen_frd(const double x, const double y, const double z)
{
    return 4 * std::cos(x) * std::cos(y) * std::cos(z)
        - (std::cos(2 * x) * std::cos(2 * y) + std::cos(2 * y) * std::cos(2 * z)
           + std::cos(2 * z) * std::cos(2 * x));
}

inline double PMY(const double x, const double y, const double z)
{
    return 2 * std::cos(x) * std::cos(y) * std::cos(z)
        + std::sin(2 * x) * std::sin(y) + std::sin(x) * std::sin(2 * z)
        + std::sin(2 * y) * std::sin(z);
}

inline double tubular_G_AB(const double x, const double y, const double z)
{
    return 20
        * (std::cos(x) * std::sin(y) + std::cos(y) * std::sin(z)
           + std::cos(z) * std::sin(x))
        - 0.5
        * (std::cos(2 * x) * std::cos(2 * y) + std::cos(2 * y) * std::cos(2 * z)
           + std::cos(2 * z) * std::cos(2 * x))
        - 4;
}

inline double tubular_G_C(const double x, const double y, const double z)
{
    return -10
        * (std::cos(x) * std::sin(y) + std::cos(y) * std::sin(z)
           + std::cos(z) * std::sin(x))
        + 2
        * (std::cos(2 * x) * std::cos(2 * y) + std::cos(2 * y) * std::cos(2 * z)
           + std::cos(2 * z) * std::cos(2 * x))
        + 12;
}

inline double BCC(const double x, const double y, const double z)
{
    return std::cos(x) + std::cos(y) + std::cos(z)
        - 2
        * (std::cos(x / 2) * std::cos(y / 2) + std::cos(y / 2) * std::cos(z / 2)
           + std::cos(z / 2) * std::cos(x / 2));
}

} // namespace tpms