import sys
sys.path.append('./output')

import antlr3
import antlr3.tree
from myhdlLexer import myhdlLexer
from myhdlParser import myhdlParser
from Eval import Eval

char_stream = antlr3.ANTLRInputStream(sys.stdin)
lexer = myhdlLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = myhdlParser(tokens)
r = parser.prog()

## Get root of the tree
root = r.tree

nodes = antlr3.tree.CommonTreeNodeStream(root)
nodes.setTokenStream(tokens)
eval = Eval(nodes)
eval.prog()
