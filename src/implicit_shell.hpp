#pragma once

#include "implicit.hpp"

namespace tpms {

class ImplicitShell {
public:
    ImplicitShell(const Implicit& f, double thickness)
        : f(f)
        , m_thickness(thickness)
    {
    }

    double operator()(double x, double y, double z) const
    {
        const double S = f(x, y, z);
        const Eigen::Vector3d dS = f.gradient(x, y, z);
        const double t = thickness() / 2 * dS.norm();
        return (S - t) * (S + t);
    }

    Eigen::VectorXd operator()(
        const Eigen::VectorXd& x,
        const Eigen::VectorXd& y,
        const Eigen::VectorXd& z) const
    {
        Eigen::VectorXd result(x.size());
        for (int i = 0; i < x.size(); ++i) {
            result(i) = (*this)(x(i), y(i), z(i));
        }
        return result;
    }

    const Eigen::Array3d& domain() const { return f.domain(); }
    double thickness() const { return m_thickness; }

private:
    Implicit f;
    double m_thickness;
};

} // namespace tpms