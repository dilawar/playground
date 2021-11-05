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
#include <thread>
#include <cstdio>
#include <iostream>

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

int main()
{
    std::thread f(test);
    f.detach();
    return 0;
}
