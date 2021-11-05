// =====================================================================================
//
//       Filename:  fiber.cpp
//
//    Description:  Playing with boost fiber.
//
//         Author:  Dilawar Singh (), dilawar@subcom.tech
//   Organization:  Subconscious Compute
//
// =====================================================================================

#include <boost/fiber/all.hpp>
#include <chrono>
#include <cstdio>
#include <iostream>
#include <thread>

using namespace std;

void
print_a()
{
    printf("a");
    boost::this_fiber::yield();
}

void
print_b()
{
    printf("b");
    std::thread j([]() { printf("N"); });
    j.detach();
    boost::this_fiber::yield();
}

int
test()
{
    boost::fibers::fiber([]() {
        do {
            print_a();
        } while (true);
    }).detach();

    boost::fibers::fiber([]() {
        do {
            print_b();
        } while (true);
    }).detach();

    printf("xxxx");

    return 0;
}

int
main()
{
    test();
    return 0;
}
