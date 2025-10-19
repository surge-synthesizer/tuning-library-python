cmake_minimum_required(VERSION 3.15...3.26)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(tuning_library VERSION "0.0.1")

# Define CMAKE_INSTALL_xxx: LIBDIR, INCLUDEDIR
include(GNUInstallDirs)
include(FetchContent)

find_package(pybind11 CONFIG REQUIRED)

set(python_module_name _tuning_library)
pybind11_add_module(${python_module_name} MODULE
  src/tuning_library/tuning_library.cpp
)

target_include_directories(${python_module_name} PUBLIC libs/tuning-library/include)

install(TARGETS ${python_module_name} DESTINATION tuning_library)
