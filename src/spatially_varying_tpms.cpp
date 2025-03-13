#include "spatially_varying_tpms.hpp"

#include "tpms.hpp"
#include "tpms_gradient.hpp"
#include "interpolated_tpms.hpp"

#include <cassert>
#include <iostream>

namespace tpms {

namespace {
    double sigmoid(const double x, const double f = 1)
    {
        return 1 / (1 + std::exp(-f * x));
    }

    double sigmoid_gradient(const double x, const double f = 1)
    {
        double s = sigmoid(x, f);
        return f * s * (1 - s);
    }
} // namespace

SpatiallyVaryingTPMS::SpatiallyVaryingTPMS() : Implicit()
{
    this->m_domain = 4 * TPMS_DOMAIN;
    const double dx = 0; // this->m_domain[0] / 2;
    const double dy = 0; // this->m_domain[1] / 2;
    const double dz = 0; // this->m_domain[2] / 2;

    this->f = [dx, dy, dz](double x, double y, double z) {
        double r = 0;
        for (int i = 0; i < 8; ++i) {
            r += sigmoid((2 * ((4 & i) >> 2) - 1) * (x - dx))
                * sigmoid((2 * ((2 & i) >> 1) - 1) * (y - dy))
                * sigmoid((2 * ((1 & i) >> 0) - 1) * (z - dz))
                * InterpolatedTPMS::TPMSs[i](x, y, z);
        }
        return r;
    };

    this->df = [dx, dy, dz](double x, double y, double z) {
        Eigen::Vector3d r = Eigen::Vector3d::Zero();
        for (int i = 0; i < 8; ++i) {
            const double sigmoid_x =
                sigmoid((2 * ((4 & i) >> 2) - 1) * (x - dx));
            const double sigmoid_y =
                sigmoid((2 * ((2 & i) >> 1) - 1) * (y - dy));
            const double sigmoid_z =
                sigmoid((2 * ((1 & i) >> 0) - 1) * (z - dz));

            const double f = InterpolatedTPMS::TPMSs[i](x, y, z);
            const Eigen::Vector3d grad_f =
                InterpolatedTPMS::TPMSs[i].gradient(x, y, z);

            r += sigmoid_x * sigmoid_y * sigmoid_z * grad_f
                + sigmoid_gradient((2 * ((4 & i) >> 2) - 1) * (x - dx))
                    * sigmoid_y * sigmoid_z * f * Eigen::Vector3d::UnitX()
                + sigmoid_x
                    * sigmoid_gradient((2 * ((2 & i) >> 1) - 1) * (y - dy))
                    * sigmoid_z * f * Eigen::Vector3d::UnitY()
                + sigmoid_x * sigmoid_y
                    * sigmoid_gradient((2 * ((1 & i) >> 0) - 1) * (z - dz)) * f
                    * Eigen::Vector3d::UnitZ();
        }
        return r;
    };
}

} // namespace tpms