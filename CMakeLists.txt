cmake_minimum_required(VERSION 3.15...3.26)

project(tuning_library VERSION "0.0.0")

# Define CMAKE_INSTALL_xxx: LIBDIR, INCLUDEDIR
include(GNUInstallDirs)
include(FetchContent)

FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/tags/v2.10.4.tar.gz
  URL_HASH SHA256=832e2f309c57da9c1e6d4542dedd34b24e4192ecb4d62f6f4866a737454c9970
)
FetchContent_MakeAvailable(pybind11)

set(python_module_name _tuning_library)
pybind11_add_module(${python_module_name} MODULE
  src/tuning_library/tuning_library.cpp
)

target_include_directories(${python_module_name} PUBLIC libs/tuning-library/include)

install(TARGETS ${python_module_name} DESTINATION tuning_library)
