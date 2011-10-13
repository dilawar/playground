"""
Dilawar Singh, IITB, 2011

REF : Simple Python NodeVisitor Example from codemonkey.blogspot.com

"""

import ast

class FirstParser(ast.NodeVisitor):

    def __init__(self):
        pass
        
    
    def continueT(self, stmt):
        ''' Helper: Pass a node children '''
        super(FirstParser, self).generic_visit(stmt)


    def parse(self, code):
        ''' Parse the code into a tree and walk the result.'''
        tree = ast.parse(code)
        self.visit(tree)


    def visitImport(self, stmt_import):
        ''' Retrieve the name from the returned objects. Normally there is just
        a single alias'''
        for alias in stmt_import.names:
            print 'import name "%s"' % alias.name
            print 'import object %s' % alias

        self.continueT(stmt_binop)


    def visitBinop(self, stmt_binop):
        print 'expression: '

        for child in ast.iter_fields(stmt_binop):
            print '   child %s ' % str(child)

        self.continueT(stmp_binop)


class myhdlNodeVisitor(ast.NodeVisitor):

    def __init__(self):
        pass
    
    def myhdl_visit(self, node):
        print type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)

        
