#pragma once

#include <Eigen/Dense>

namespace tpms {

inline Eigen::Vector3d
schoen_gyroid_gradient(const double x, const double y, const double z)
{
    const double t0 = sin(x);
    const double t1 = sin(z);
    const double t2 = cos(x);
    const double t3 = cos(y);
    const double t4 = sin(y);
    const double t5 = cos(z);
    return Eigen::Vector3d(
        -t0 * t1 + t2 * t3, -t0 * t4 + t3 * t5, -t1 * t4 + t2 * t5);
}

inline Eigen::Vector3d
schwarz_diamond_gradient(const double x, const double y, const double z)
{
    const double t0 = cos(z);
    const double t1 = cos(y);
    const double t2 = sin(x);
    const double t3 = t1 * t2;
    const double t4 = sin(z);
    const double t5 = cos(x);
    const double t6 = sin(y);
    const double t7 = t5 * t6;
    return Eigen::Vector3d(
        -t0 * t3 - t4 * t7, -t0 * t7 - t3 * t4, -t0 * t2 * t6 - t1 * t4 * t5);
}

inline Eigen::Vector3d
schwarz_primitive_gradient(const double x, const double y, const double z)
{
    return Eigen::Vector3d(-sin(x), -sin(y), -sin(z));
}

inline Eigen::Vector3d
schoen_iwp_gradient(const double x, const double y, const double z)
{
    const double t0 = sin(x);
    const double t1 = cos(y);
    const double t2 = cos(z);
    const double t3 = sin(y);
    const double t4 = cos(x);
    const double t5 = sin(z);
    return Eigen::Vector3d(
        -2 * t0 * t1 - 2 * t0 * t2 + 2 * sin(2 * x),
        -2 * t2 * t3 - 2 * t3 * t4 + 2 * sin(2 * y),
        -2 * t1 * t5 - 2 * t4 * t5 + 2 * sin(2 * z));
}

inline Eigen::Vector3d
neovius_gradient(const double x, const double y, const double z)
{
    const double t0 = cos(y);
    const double t1 = 4 * cos(z);
    const double t2 = cos(x);
    return Eigen::Vector3d(
        -(t0 * t1 + 3) * sin(x), -(t1 * t2 + 3) * sin(y),
        -(4 * t0 * t2 + 3) * sin(z));
}

inline Eigen::Vector3d
fischer_koch_s_gradient(const double x, const double y, const double z)
{
    const double t0 = sin(x);
    const double t1 = sin(z);
    const double t2 = 2 * y;
    const double t3 = cos(t2);
    const double t4 = sin(y);
    const double t5 = cos(z);
    const double t6 = 2 * x;
    const double t7 = cos(x);
    const double t8 = cos(y);
    const double t9 = 2 * z;
    const double t10 = cos(t9);
    const double t11 = cos(t6);
    return Eigen::Vector3d(
        -t0 * t1 * t3 + t10 * t7 * t8 - 2 * t4 * t5 * sin(t6),
        -t0 * t10 * t4 - 2 * t1 * t7 * sin(t2) + t11 * t5 * t8,
        -2 * t0 * t8 * sin(t9) - t1 * t11 * t4 + t3 * t5 * t7);
}

inline Eigen::Vector3d
schoen_frd_gradient(const double x, const double y, const double z)
{
    const double t0 = cos(y);
    const double t1 = 2 * cos(z);
    const double t2 = 2 * x;
    const double t3 = sin(t2);
    const double t4 = 2 * y;
    const double t5 = cos(t4);
    const double t6 = 2 * z;
    const double t7 = cos(t6);
    const double t8 = cos(x);
    const double t9 = sin(t4);
    const double t10 = cos(t2);
    const double t11 = sin(t6);
    return Eigen::Vector3d(
        -2 * t0 * t1 * sin(x) + 2 * t3 * t5 + 2 * t3 * t7,
        -2 * t1 * t8 * sin(y) + 2 * t10 * t9 + 2 * t7 * t9,
        -4 * t0 * t8 * sin(z) + 2 * t10 * t11 + 2 * t11 * t5);
}

inline Eigen::Vector3d
PMY_gradient(const double x, const double y, const double z)
{
    const double t0 = cos(x);
    const double t1 = 2 * z;
    const double t2 = 2 * x;
    const double t3 = 2 * sin(y);
    const double t4 = cos(y);
    const double t5 = cos(z);
    const double t6 = 2 * sin(x);
    const double t7 = 2 * y;
    const double t8 = 2 * sin(z);
    return Eigen::Vector3d(
        t0 * sin(t1) + t3 * cos(t2) - t4 * t5 * t6,
        -t0 * t3 * t5 + t4 * sin(t2) + t8 * cos(t7),
        -t0 * t4 * t8 + t5 * sin(t7) + t6 * cos(t1));
}

} // namespace tpms