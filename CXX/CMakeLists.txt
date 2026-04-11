cmake_minimum_required(VERSION 3.10)
project(CXX_Playground LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Collect all .cpp files in src/
file(GLOB SOURCES "src/*.cpp")

# Create an executable for each .cpp file
foreach(SOURCE ${SOURCES})
    get_filename_component(FILE_NAME ${SOURCE} NAME_WE)
    add_executable(${FILE_NAME} ${SOURCE})
endforeach()
