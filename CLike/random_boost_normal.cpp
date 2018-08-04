#include <iostream>
#include <random>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/normal_distribution.hpp>


int main(int argc, const char *argv[])
{

    // Initialize seed .
    std::mt19937 gena;
    boost::random::mt19937 genb;
    gena.seed( 10 );
    genb.seed( 10 );

    std::normal_distribution<> norma;
    boost::random::normal_distribution<> normb;

    std::cout << "STD BOOST" << std::endl;
    for (size_t i = 0; i < 20; i++) 
        std::cout << norma(gena) << ' ' << normb(genb) << std::endl;

    return 0;
}

