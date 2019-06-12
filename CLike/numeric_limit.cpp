/*
 * =====================================================================================
 *
 *       Filename:  numeric_limit.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Monday 17 September 2018 10:11:03  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <iostream>
#include <cmath>
#include <numeric>
#include <limits>

using namespace std;


int main(int argc, const char *argv[])
{
    double eps = numeric_limits<double>::epsilon();
    cout << "EPS: " << eps <<  ' ' << sqrt(eps) << endl;
    return 0;
}

