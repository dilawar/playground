/*
 * =====================================================================================
 *
 *       Filename:  compare.c
 *
 *    Description:  Compare integers.
 *
 *        Version:  1.0
 *        Created:  Wednesday 19 October 2011 09:46:21  IST
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
    printf("Is 2 and 2.00 are same %d\n", (2 == 2.00));
    printf("Is int 2 and double 2 are same %d\n", ((int)2 == (double)2));
    printf("Is int 2 and char 2 are same %d\n", ((int)2 == '2'));
    return 0;
}
