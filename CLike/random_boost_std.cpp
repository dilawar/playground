#include <iostream>
#include <random>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_01.hpp>
#include <boost/random/uniform_real_distribution.hpp>


int main(int argc, const char *argv[])
{

    // Initialize seed .
    std::mt19937 gena( 1 );
    boost::random::mt19937 genb( 1 );

    std::uniform_real_distribution<> dista(0, 1);
    boost::random::uniform_01<> distb;
    boost::random::uniform_real_distribution<> distc(0,1);
    

    double ra, rb = 0.0;
    for (size_t i = 0; i < 10; i++) 
        std::cout << dista(gena) << ' ' << distb(genb) << ' ' << distc(genb) << std::endl;

    return 0;
}

