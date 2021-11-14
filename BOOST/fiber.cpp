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
#include <iostream>
#include <thread>

using namespace std;

void print_a()
{
    cout << "a";
    boost::this_fiber::yield();
}

void print_b()
{
    cout << "b";
    std::thread j([]() { printf("B"); });
    j.detach();
    boost::this_fiber::yield();
}

int main()
{
    int i = 0;
    boost::fibers::fiber([&]() {
        do {
            print_a();
            i++;
        }
        while (i < 20)
            ;
    }).detach();

    boost::fibers::fiber([&]() {
        do {
            i++;
            print_b();
        } while (i < 20);
    }).detach();

    printf("X");
    return 0;
}
