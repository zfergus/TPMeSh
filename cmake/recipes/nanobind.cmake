# nanobind (https://github.com/wjakob/nanobind)
# License: BSD-style
if(TARGET nanobind::nanobind)
    return()
endif()

message(STATUS "Third-party: creating target 'nanobind::nanobind'")

if (POLICY CMP0094)  # https://cmake.org/cmake/help/latest/policy/CMP0094.html
    cmake_policy(SET CMP0094 NEW)  # FindPython should return the first matching Python
endif ()

# needed on GitHub Actions CI: actions/setup-python does not touch registry/frameworks on Windows/macOS
# this mirrors PythonInterp behavior which did not consult registry/frameworks first
if (NOT DEFINED Python_FIND_REGISTRY)
    set(Python_FIND_REGISTRY "LAST")
endif ()
if (NOT DEFINED Python_FIND_FRAMEWORK)
    set(Python_FIND_FRAMEWORK "LAST")
endif ()

# Nanobind still uses the deprecated FindPythonInterp. So let's call CMake's
# new FindPython module and set PYTHON_EXECUTABLE for Nanobind to pick up.
# This works well with conda environments.
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
set(PYTHON_EXECUTABLE ${Python_EXECUTABLE})

include(CPM)
CPMAddPackage("gh:wjakob/nanobind@1.9.2")
