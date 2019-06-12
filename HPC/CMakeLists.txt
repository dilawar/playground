cmake_minimum_required(VERSION 3.0)

# NOTE: On OpenSUE, have a look here 
# https://flanaras.wordpress.com/2017/01/31/setup-opencl-on-opensuse-intel-integrated-gpu/

project(test_hpc)

find_package(OpenCL REQUIRED)

include_directories(${OpenCL_INCLUDE_DIRS})

add_executable(test_boost_compute ./test_boost_compute_core.cpp)

target_link_libraries(test_boost_compute ${OpenCL_LIBRARIES})

