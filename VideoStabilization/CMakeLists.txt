cmake_minimum_required(VERSION 2.8)
project(videostab)

set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules 
    )

add_definitions( -std=c++11 -Wall )

set(CMAKE_BUILD_TYPE Release )

find_package( OPENCV REQUIRED 
    COMPONENTS core highgui imgcodecs videoio imgproc calib3d video
    )
find_package( TIFF REQUIRED )
#find_package( GSL REQUIRED )


add_executable(videostab src/main.cpp)

target_link_libraries( videostab  
    ${TIFF_LIBRARIES}
    #${GSL_LIBRARIES}
    ${OPENCV_LIBRARIES}
    )
