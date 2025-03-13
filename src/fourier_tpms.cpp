#include "fourier_tpms.hpp"

#include "tpms.hpp"
#include "tpms_gradient.hpp"

#include <iostream>

namespace tpms {

FourierTPMS::FourierTPMS() : Implicit()
{
    constexpr int N = 4;
    constexpr double FREQUENCY = 1 / (2 * M_PI);

    this->m_domain = TPMS_DOMAIN;

    this->f = [](double x, double y, double z) {
        double r = 0;
        for (int k = 1; k <= N; ++k) {
            r += schoen_gyroid(2 * M_PI * (2 * k - 1) * FREQUENCY * x, y, z)
                / (2 * k - 1);
        }
        return (4 / M_PI) * r;
    };

    this->df = [](double x, double y, double z) -> Eigen::Vector3d {
        Eigen::Vector3d r = Eigen::Vector3d::Zero();
        for (int k = 1; k <= N; ++k) {
            const double tmp = 2 * M_PI * (2 * k - 1) * FREQUENCY;
            Eigen::Vector3d g =
                schoen_gyroid_gradient(tmp * x, y, z) / (2 * k - 1);
            g[0] *= tmp;
            r += g;
        }
        return (4 / M_PI) * r;
    };
}

} // namespace tpms