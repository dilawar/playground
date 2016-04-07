/*
 * =====================================================================================
 *
 *       Filename:  example1.cpp
 *
 *    Description:  Parallel for
 *
 *        Version:  1.0.0
 *        Created:  04/07/2016 10:25:12 AM
 *       Compiler:  g++ 
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 *  NOTES:
 *
 *   To compile: 
 *      
 *      g++ -fopenmp example1.cpp -o example1
 *   
 *   To run,
 *      ./example1
 *
 * =====================================================================================
 */

#include <iostream>
#include <cstdio>

#include <omp.h>



using namespace std;

int main(int argc, const char *argv[])
{

    // Let's create the team of thread first.
#pragma omp parallel
    {
        /* Handles different portion of the loop */
        #pragma omp for  
        for (int i = 0; i < 10; i++) {
            printf( "Thread %d : %d\n", omp_get_thread_num(), i); 
        }
    }
    printf( "Done" );
    return 0;
}
