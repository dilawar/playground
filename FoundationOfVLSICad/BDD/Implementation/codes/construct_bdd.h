/* (c) 2011 GNU GPL
 * Dilawar Singh 
 * Email : dilawar@ee.iitb.ac.in
 * Indian Institute of Technology Bombay
 */


#ifndef CONSTRUCT_BDD_H
#define CONSTRUCT_BDD_H
typedef unsigned int addr;
#define addr_ (p) ((addr)(size_t)(p))
#define logPageSize        12
#define memSize            (1<<29)
#define pageSize           (1<<logPageSize) /* bytes per page */
#define pageMask           (pageSize-1)
#define pageInts           pageSize/sizeof(int)
#define bddNode_ (a)       ((bddNode*)(size_t)(a))
#define page_ (a)          ((page*)(size_t)(a))


typedef struct nodeStruct
{
    addr lo, hi;
    int varRef;
    unsigned int index; /* variable id followed by random bits. */
} bddNode;

typedef struct pageStruct
{
    addr dat[pageInts];
} page;


#define FILEPATH_MAX    100
#define NAME_MAX        100
#define VAR_SIZE        4        /* variable in BDD expr */
#define OP_SIZE         4        /* Binary operation in BDD expr */
#define ZERO            0
#define ONE             1

struct bddExpression             /* structure for binary expressions. */
{
    struct bddExpression *lBddExpr;
    struct bddExpression *rBddExpr;
    char* binOp;
    char *lVar, *rVar; 
};


/* Function to read my BDD expression file. */
struct bddExpression* readBDDFile (char*);

#endif


