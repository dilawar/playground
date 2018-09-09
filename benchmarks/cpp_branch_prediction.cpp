/*
 * =====================================================================================
 *
 *       Filename:  cpp_branch_prediction.cpp
 *
 *    Description:  Branch perdiction.
 *
 *        Version:  1.0
 *        Created:  Sunday 09 September 2018 02:13:15  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 *   NOTE:
 *
 *   No differences between if elsif on sorted or unsorted vector.
 *
 * =====================================================================================
 */

#include <random>
#include <iostream>
#include <chrono>
#include <vector>
#include <ctime>
#include <algorithm>

using namespace std;
using namespace std::chrono;

inline double do_step( double x )
{
    double res = 0;
    if( x < 10 )
        res += 1;
    else if( x < 20 )
        res += 1;
    else if( x < 30 )
        res += 1;
    else if( x < 40 )
        res += 1;
    else if( x < 50 )
        res += 1;
    else if( x < 60 )
        res += 1;
    else if( x < 70 )
        res += 1;
    else
        res += 1;

    return res;
}

int main(int argc, const char *argv[])
{
    size_t N = 3*pow(10, 8);
    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0,100); 

    vector<double> nums;
    for (size_t i = 0; i < N; i++) 
        nums.push_back( dist(rng) );

    std::cout << N << " numbers generated." << std::endl;

    clock_t c = clock();
    double r = 0;
    for( auto x : nums )
        r += do_step( x );
    cout << r << " Time taken without sort " <<(double)(clock() - c)/CLOCKS_PER_SEC << endl;

    r = 0;
    sort( nums.begin(), nums.end() );
    c = clock();
    for( auto x : nums )
        r += do_step( x );
    cout << r << " Time taken without sort " <<(double)(clock() - c)/CLOCKS_PER_SEC << endl;

    return 0;
}

