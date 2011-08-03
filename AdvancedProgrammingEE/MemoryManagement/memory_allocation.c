/*
 * =====================================================================================
 *
 *       Filename:  memory_allocation.c
 *
 *    Description:  Written to learn how memory allocation is done.
 *
 *        Version:  1.0
 *        Created:  Thursday 04 August 2011 12:24:55  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (Graduate Student, EE IITB), dilawar@ee.iitb.ac.in
 *      Institute:  IIT Bombay
 *
 * =====================================================================================
 */


#include	<stdio.h>

typedef long Align;

union header {
    struct {
        union header *ptr;
        unsigned size;
    } s;
    Align x;
};

typedef union header Header;

int main ()
{
    Header *p, *prevp;
    printf("Size of my union is : %d, and struct is : %d \n", sizeof(Header), sizeof(p->s));
    printf("Size of pointer to header is %d ", sizeof(p->s.ptr)); 
    return 0;
}
