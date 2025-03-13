#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/function.h>
#include <nanobind/eigen/dense.h>

#include <Eigen/Core>

#include "tpms.hpp"
#include "tpms_gradient.hpp"
#include "implicit.hpp"
#include "implicit_shell.hpp"
#include "interpolated_tpms.hpp"
#include "spatially_varying_tpms.hpp"
#include "fourier_tpms.hpp"

namespace nb = nanobind;

#define BIND_3D_FUNCTION(NAME)                                                 \
    m.def(#NAME, &tpms::NAME, nb::arg("x"), nb::arg("y"), nb::arg("z"))

NB_MODULE(_tpms, m)
{
    using namespace tpms;

    m.doc() = "Triply periodic minimal surfaces (TPMS)";

    // TPMS functions
    BIND_3D_FUNCTION(schoen_gyroid);
    BIND_3D_FUNCTION(double_schoen_gyroid);
    BIND_3D_FUNCTION(schwarz_diamond);
    BIND_3D_FUNCTION(double_swartz_diamond);
    BIND_3D_FUNCTION(schwarz_primitive);
    BIND_3D_FUNCTION(double_schwarz_primitive);
    BIND_3D_FUNCTION(schoen_iwp);
    BIND_3D_FUNCTION(lipnoid);
    BIND_3D_FUNCTION(neovius);
    BIND_3D_FUNCTION(fischer_koch_s);
    BIND_3D_FUNCTION(schoen_frd);
    BIND_3D_FUNCTION(PMY);
    BIND_3D_FUNCTION(tubular_G_AB);
    BIND_3D_FUNCTION(tubular_G_C);
    BIND_3D_FUNCTION(BCC);

    // Gradient functions
    BIND_3D_FUNCTION(schoen_gyroid_gradient);
    BIND_3D_FUNCTION(schwarz_diamond_gradient);
    BIND_3D_FUNCTION(schwarz_primitive_gradient);
    BIND_3D_FUNCTION(schoen_iwp_gradient);
    BIND_3D_FUNCTION(neovius_gradient);
    BIND_3D_FUNCTION(fischer_koch_s_gradient);
    BIND_3D_FUNCTION(schoen_frd_gradient);
    BIND_3D_FUNCTION(PMY_gradient);

    nb::class_<Implicit>(m, "Implicit")
        .def(
            nb::init<
                const std::function<double(double, double, double)>&,
                const std::function<Eigen::Vector3d(double, double, double)>&,
                const Eigen::Array3d&>(),
            nb::arg("f"), nb::arg("df"), nb::arg("domain"))
        .def(
            "__call__",
            nb::overload_cast<double, double, double>(
                &Implicit::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "__call__",
            nb::overload_cast<
                const Eigen::VectorXd&, const Eigen::VectorXd&,
                const Eigen::VectorXd&>(&Implicit::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "eval",
            nb::overload_cast<double, double, double>(
                &Implicit::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "eval",
            nb::overload_cast<
                const Eigen::VectorXd&, const Eigen::VectorXd&,
                const Eigen::VectorXd&>(&Implicit::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "gradient", &Implicit::gradient, nb::arg("x"), nb::arg("y"),
            nb::arg("z"))
        .def_prop_ro("domain", &Implicit::domain);

    nb::class_<ImplicitShell>(m, "ImplicitShell")
        .def(nb::init<Implicit, double>(), nb::arg("f"), nb::arg("thickness"))
        .def(
            "__call__",
            nb::overload_cast<double, double, double>(
                &ImplicitShell::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "__call__",
            nb::overload_cast<
                const Eigen::VectorXd&, const Eigen::VectorXd&,
                const Eigen::VectorXd&>(&ImplicitShell::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "eval",
            nb::overload_cast<double, double, double>(
                &ImplicitShell::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def(
            "eval",
            nb::overload_cast<
                const Eigen::VectorXd&, const Eigen::VectorXd&,
                const Eigen::VectorXd&>(&ImplicitShell::operator(), nb::const_),
            nb::arg("x"), nb::arg("y"), nb::arg("z"))
        .def_prop_ro("thickness", &ImplicitShell::thickness)
        .def_prop_ro("domain", &ImplicitShell::domain);

    nb::class_<InterpolatedTPMS, Implicit>(m, "InterpolatedTPMS")
        .def(nb::init<const Eigen::ArrayXd&>(), nb::arg("params"))
        .def_ro_static("TPMSs", &InterpolatedTPMS::TPMSs);

    nb::class_<SpatiallyVaryingTPMS, Implicit>(m, "SpatiallyVaryingTPMS")
        .def(nb::init<>());

    nb::class_<FourierTPMS, Implicit>(m, "FourierTPMS").def(nb::init<>());
}
