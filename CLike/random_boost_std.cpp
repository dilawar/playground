#include <iostream>
#include <random>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_01.hpp>
#include <boost/random/uniform_real_distribution.hpp>


int main(int argc, const char *argv[])
{

    // Initialize seed .
    std::mt19937 gena;
    gena.seed( 5489UL );
    boost::random::mt19937 genb;
    genb.seed( 5489UL );

    std::uniform_real_distribution<> dista(0, 1);
    std::normal_distribution<> ndist(0,1);

    boost::random::uniform_01<> distb;
    boost::random::uniform_real_distribution<> distc(0,1);

    

    // double ra, rb = 0.0;
    std::cout << "STD BOOST1 BOOST2 NORMAL" << std::endl;
    for (size_t i = 0; i < 20; i++) 
        std::cout << dista(gena) << ' ' << distb(genb) << ' ' << distc(genb) 
            << ndist( gena ) << std::endl;

    return 0;
}

