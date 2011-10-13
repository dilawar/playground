""" 
example.py
dilawar, 2011
dilawar@ee.iitb.ac.in

This is a python script to generate abstract syntaxt tree from a source code.
"""
#from myhdl import *

expr = '''
ACTIVE_LOW, INACTIVE_HIGH = 0, 1

def Inc(count, enable, clock, reset, n):

    @always(clock.posedge, reset.negedge)
    def incLogic():
        if reset == ACTIVE_LOW:
            acount.next = 0
        else:
            if enable:
                count.next = (count + 1) % n

    return incLogic
'''

#def bin2gray(B, G, width):
#
#    @always_comb
#    def logic():
#        Bext = intbv(0)[width+1:]
#        Bext[:] = B
#        for i in range(width):
#            G.next[i] = Bext[i+1] ^ Bext[i]
#    return logic

## LETS PARSE THE ABOVE CODE.
import ast

# import compiler
# import codegen # Do we need it?
# import conversion_examples

from my_parser import *

"""
The mode must be  exec to compile a module, single to compile a single
(interactive) statement, or eval to compile an expression.
"""
tree = ast.parse(expr, mode= 'exec')
#print ast.dump(tree)

#n = ast.NodeVisitor();
#n.visit(tree.target)

### THIS USES myhdlNodeVisitor CLASS.
v = myhdlNodeVisitor()
v.visit(tree)

### THIS USES FirstParser CLASS
#v = FirstParser()
#v.parse(expr)
#v.continueT(expr)

#genTree = ast.walk(tree)
#for i in genTree:
#    print i._fields
#    #print dir(i)
#

