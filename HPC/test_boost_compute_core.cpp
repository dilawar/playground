// =====================================================================================
//
//       Filename:  test_boost_compute_core.cpp
//
//    Description:  
//
//        Version:  1.0
//        Created:  06/12/2019 09:52:44 AM
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar.s.rajput@gmail.com
//   Organization:  NCBS Bangalore
//
// =====================================================================================

#include <iostream>

#include <boost/compute/core.hpp>

namespace compute = boost::compute;

int main()
{
    // get the default device
    compute::device device = compute::system::default_device();

    // print the device's name and platform
    std::cout << "hello from " << device.name();
    std::cout << " (platform: " << device.platform().name() << ")" << std::endl;

    return 0;
}
