#include "interpolated_tpms.hpp"

#include "tpms.hpp"
#include "tpms_gradient.hpp"

#include <cassert>
#include <iostream>

namespace tpms {

const std::vector<Implicit> InterpolatedTPMS::TPMSs = { {
    Implicit(schoen_gyroid, schoen_gyroid_gradient, TPMS_DOMAIN),
    Implicit(schwarz_diamond, schwarz_diamond_gradient, TPMS_DOMAIN),
    Implicit(schwarz_primitive, schwarz_primitive_gradient, TPMS_DOMAIN),
    Implicit(schoen_iwp, schoen_iwp_gradient, TPMS_DOMAIN),
    Implicit(neovius, neovius_gradient, TPMS_DOMAIN),
    Implicit(fischer_koch_s, fischer_koch_s_gradient, TPMS_DOMAIN),
    Implicit(schoen_frd, schoen_frd_gradient, TPMS_DOMAIN),
    Implicit(PMY, PMY_gradient, TPMS_DOMAIN),
} };

InterpolatedTPMS::InterpolatedTPMS(const Eigen::ArrayXd& params) : Implicit()
{
    assert(params.size() == TPMSs.size());
    assert((0 <= params).all() && (params <= 1).all());
    assert(std::abs(params.sum() - 1.0) < 1e-10);

    std::vector<size_t> nonzero_indices;
    for (size_t i = 0; i < params.size(); ++i) {
        if (params[i] != 0) {
            nonzero_indices.push_back(i);
        }
    }

    std::vector<double> _params;
    std::vector<Implicit> _tpms;

    _params.reserve(nonzero_indices.size());
    _tpms.reserve(nonzero_indices.size());

    for (size_t i : nonzero_indices) {
        _params.push_back(params[i]);
        _tpms.push_back(TPMSs[i]);
    }

    this->f = [_params, _tpms](double x, double y, double z) {
        double result = 0.0;
        for (size_t i = 0; i < _params.size(); ++i) {
            result += _params[i] * _tpms[i](x, y, z);
        }
        return result;
    };

    this->df = [_params, _tpms](double x, double y, double z) {
        Eigen::Vector3d result = Eigen::Vector3d::Zero();
        for (size_t i = 0; i < _params.size(); ++i) {
            result += _params[i] * _tpms[i].gradient(x, y, z);
        }
        return result;
    };

    this->m_domain = Eigen::Array3d::Zero();
    for (const Implicit& tpms : _tpms) {
        this->m_domain = this->m_domain.max(tpms.domain());
    }
}

} // namespace tpms