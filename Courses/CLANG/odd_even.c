/*
 * =====================================================================================
 *
 *       Filename:  odd_even.c
 *
 *    Description:  Let's make C go crazy.
 *
 *        Version:  1.0
 *        Created:  Friday 04 November 2011 02:41:55  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (Graduate Student, EE IITB), dilawar@ee.iitb.ac.in
 *      Institute:  IIT Bombay
 *
 * =====================================================================================
 */


#include	<stdio.h>

int main()
{
    int a = 12;
    //printf("Negating of a(%d) is %d", a, !(!a));
    printf("a is : %d", isEven(a));
    return 0;
}

int isEven(int p)
{
    int q = !isOdd(p);
    return q;
}

int isOdd(int p)
{
    int q  = !isEven(p);
    return q;
}
