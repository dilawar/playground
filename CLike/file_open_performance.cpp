/*
 * =====================================================================================
 *
 *       Filename:  file_open_performance.cpp
 *
 *    Description:  benchmakr  file open/close 
 *
 *        Version:  1.0
 *        Created:  05/01/2016 02:39:35 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <iostream>
#include <fstream>
#include <chrono>

using namespace std;

int main(int argc, const char *argv[])
{
    ofstream of_;
    of_.open( "a.txt" );
    auto t1 = chrono::system_clock::now();
    for (size_t i = 0; i < 1e6; i++) 
        of_ << "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" << endl;
    of_.close();
    chrono::duration<double> duration = chrono::system_clock::now() - t1;
    cerr << "1 open/ 1 close, time taken " << duration.count()
        << " seconds " << endl;
    
    // Now open every time and close it.
    t1 = chrono::system_clock::now();
    for (size_t i = 0; i < 1e6; i++) 
    {
        of_.open( "b.txt", ios::app );
        of_ << "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" << endl;
        of_.close();
    }
    duration = chrono::system_clock::now() - t1;
    cerr << "1million open/ 1million close, time taken " << duration.count()
        << " seconds " << endl;
    return 0;
}
