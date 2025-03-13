include(nanobind)
nanobind_add_module(_tpms
  bindings.cpp
  fourier_tpms.cpp
  fourier_tpms.hpp
  implicit_shell.hpp
  implicit.hpp
  interpolated_tpms.cpp
  interpolated_tpms.hpp
  spatially_varying_tpms.cpp
  spatially_varying_tpms.hpp
  tpms_gradient.hpp
  tpms.hpp
)

include(eigen)
target_link_libraries(_tpms PUBLIC Eigen3::Eigen)