#pragma once

#include <Eigen/Core>

#include <cmath>
#include <functional>

namespace tpms {

class Implicit {
protected:
    Implicit() = default;

public:
    Implicit(
        const std::function<double(double, double, double)>& f,
        const std::function<Eigen::Vector3d(double, double, double)>& df,
        const Eigen::Array3d& domain)
        : f(f)
        , df(df)
        , m_domain(domain)
    {
    }

    double operator()(double x, double y, double z) const
    {
        if (f == nullptr) {
            throw std::runtime_error("Evaluation not implemented");
        }
        return f(x, y, z);
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

    Eigen::Vector3d gradient(double x, double y, double z) const
    {
        if (df == nullptr) {
            throw std::runtime_error("Gradient not implemented");
        }
        return df(x, y, z);
    }

    const Eigen::Array3d& domain() const { return m_domain; }

protected:
    std::function<double(double, double, double)> f;
    std::function<Eigen::Vector3d(double, double, double)> df;
    Eigen::Array3d m_domain;
};

} // namespace tpms