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
 *Bombay
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
void *myMalloc(unsigned nbytes); /* general-purpose storage allocator */

static Header base; /* empty header to start with. */
static Header *freep = NULL; /* start of free list.  */

int main ()
{
  #if 1
    printf("Size of my union and its pointer : %d, %d \n", sizeof(base), sizeof(freep));
#endif
    myMalloc(10);
    printf("Calling myMalloc second time. \n");
    myMalloc(16);
    return 0;
}

void *myMalloc(unsigned nbytes) /* general-purpose storage allocator */
{
    Header *p, *prevp;
    Header *morecore(unsigned);
    unsigned nunits;

    nunits = (nbytes + sizeof(Header) - 1)/sizeof(Header) + 1;
    printf("DEBUG: sizeof(Header) and nunits : %d, %d\n", sizeof(Header), nunits);

    if((prevp = freep) == NULL)
    {
        printf("DEBUG: No free list yet. and the base address is %d\n", &base);
        base.s.ptr = freep = prevp = &base;
        base.s.size = 0;
    }

    for( p = prevp->s.ptr; ; prevp = p, p = p->s.ptr)
    {
        printf("DEBUG: p $ prevp : %d, %d\n", p , prevp);
        if( p->s.size >= nunits)
        {
            if( p->s.size == nunits)
            {
                printf("The chunck is exact.\n");
                prevp->s.ptr = p->s.ptr;
            }
            else
            {
                p->s.size -= nunits;
                p += p->s.size;
                p->s.size = nunits;
            }
            freep = prevp;
            return (void *)(p+1);
        }
        if (p == freep)
            if((p=morecore(nunits)) == NULL)
                return NULL;
    }
}

#define NALLOC 1024

/*  morecore */
static Header* morecore (unsigned nu)
{
    char *cp, *sbrk(int);
    Header *up;

    if (nu < NALLOC)
        nu = NALLOC;
    cp = sbrk(nu * sizeof(Header));
    if(cp == (char *) - 1)
        return NULL;
    up = (Header *) cp;
    up->s.size = nu;
    free((void *)(up+1));
    return freep;
}

/*  free */
void free (void *ap)
{
    Header *bp, *p;
    bp = (Header *)ap -1; /*  point to block header */

    for(p = freep; !(bp > p && bp < p->s.ptr); p = p->s.ptr)
        if(p >= p->s.ptr && (bp > p || bp < p->s.ptr))
            break; /*  free block at the start of end of arena */
    if(bp + bp->s.size == p->s.ptr)
    {
        bp->s.size +=p->s.ptr->s.size;

    }


}
