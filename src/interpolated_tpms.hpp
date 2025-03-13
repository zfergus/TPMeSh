#pragma once

#include "implicit.hpp"

#include <Eigen/Core>

#include <vector>

namespace tpms {

class InterpolatedTPMS : public Implicit {
public:
    InterpolatedTPMS(const Eigen::ArrayXd& params);

    /// @brief List of TPMSs
    static const std::vector<Implicit> TPMSs;
};

} // namespace tpms
