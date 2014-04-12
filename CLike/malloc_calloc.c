/*
 * ==============================================================================
 *
 *       Filename:  malloc_calloc.c
 *
 *    Description:  Compare time for both malloc and calloc
 *
 *        Version:  1.0
 *        Created:  Saturday 12 April 2014 11:14:51  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawar@ee.iitb.ac.in
 *   Organization:  
 *
 * ==============================================================================
 */
#include <sys/times.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct ding
{
    long long a;
    long long b;
    char* lala;
    double data;
} ding_t;

int main()
{
    clock_t t1, t2;

    struct tms pTime1, pTime2;
    unsigned long long size = (10*1024*1024);
    t1 = times(&pTime1);

    int i;
    for(i =0; i < size; i++)
    {
        malloc(size * sizeof(ding_t));
    }
    t2 = times(&pTime2);
    unsigned long long mallocTime = t2 - t1;;

    t1 = times(&pTime1);
    for(i =0; i < size; i++)
    {
        calloc(size, sizeof(ding_t));
    }
    t2 = times(&pTime2);
    unsigned long long callocTime = t2 - t1;

    printf("For allocating total of %lld in chunk size of %lld, calloc took %lld" 
            " while malloc took %lld \n"
            , size * sizeof(ding_t)
            , size
            , callocTime
            , mallocTime
          );
    return 0;
}

