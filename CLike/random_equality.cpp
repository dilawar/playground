/*
 * =====================================================================================
 *
 *       Filename:  random_equality.cpp
 *
 *    Description:  Check the effect of using >= over > in random generation.
 *
 *        Version:  1.0
 *        Created:  Tuesday 25 April 2017 09:24:03  IST
 *       Revision:  none
 *       Compiler:  g++ --std=c++11
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <iostream>
#include <random>


using namespace std;

int main(int argc, const char *argv[])
{
    double sum1 = 0.0;
    double sum2 = 0.0;

    // Initialize seed .
    random_device rd;
    std::mt19937 gen( rd() );

    uniform_real_distribution<> dist;

    double r;
    size_t n = 0;
    while( sum1 == sum2 )
    {
        r = dist( gen );
        while( r == 0.0 )
            r = dist( gen );

        if( r > 0.01 )
            sum1 += 1.0;

        if( r >= 0.01 )
            sum2 += 1.0;

        n += 1;

        if( n % 10000 == 0 )
            cout << n << endl;
    }


    std::cout << "Failed after " << n << " iteration " << std::endl;
    return 0;
}

