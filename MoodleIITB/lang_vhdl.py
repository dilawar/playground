import re
import io
import glob, os, subprocess, sys

class VHDL:

    def __init__(self):
        self.test_bench = ''
        self.component = dict()
        self.component_expr = u''
        self.port = dict()
        self.src = ''
        self.srcDir = ''

    def dirName(self, dir):
        self.srcDir = dir

    def compile_testbench(self, dir, cxx):
        '''
        This function compiles the test_bench in given directory.
        
        '''
        os.chdir(dir)
        files = glob.glob('*.vhd')
        for file in files:
                f = open(file, "r")
                if f:
                    try:
                        self.src = f.read()
                    except EOFError:
                        print "EOF"
                    if not self.src: break
                    # This will match the testbech entity in given file.
                    m = re.search(r"entity\ +(\w+)\ +is[\ \n]+end\ +(\w*)\ *\w*[;]", self.src, re.I)
                    if m : 
                        test_bench = m.group(1)
                        self.get_design(test_bench, self.src);
                        self.create_testbench(self.component, self.port)
                        print("Compiling entity {0} using {1}".format(test_bench, cxx))
                        #print("In file {0}".format(f.name))
                        #print "cxx : {0}".format(cxx)
                        if cxx == 'ghdl':
                            vcdOption = "--vcd="+test_bench+".vcd"
                            subprocess.call(["ghdl", "-a", f.name] \
                                    , stdout=subprocess.PIPE)
                            subprocess.call(["ghdl", "-m", test_bench] \
                                    , stdout=subprocess.PIPE)
                            subprocess.call(["ghdl", "-r" \
                                    , test_bench, "--stop-time=1000ns" \
                                    , vcdOption] \
                                    , stdout=subprocess.PIPE)
                        elif cxx == 'vsim' :
                            pass

                    else : 
                        pass

    def get_design(self, test_bench, data):
        print "Getting design for {0} in file {1}".format(test_bench, file)
        m = re.search(r'''component\s+(\w+)\s*(is)*\s+
                port\s*[(]
                ((\s*\w+(\s*[,]\s*\w+\s*)*\s*[:]\s*
                (in|out)\s*\w+\s*([(]\s*\d+\s*\w+\s*\d+\s*[)])*\s*[;]*)*)
                \s*[)]\s*[;]
                \s+end\s+component\s*\w*[;]'''
                , data, re.I | re.VERBOSE)

        if m:
            text = m.group(3)
            self.component_expr = text
            self.component[m.group(1)] = text
            for pExpr in text.split(';'):
                [p, expr]  = pExpr.split(':')
                p = p.strip()
                temp = expr.split()
                type = temp[0].strip()
                del temp[0]
                for i in p.split(','):
                    expr = ' '.join(temp)
                    self.port[(i, m.group(1))] = (type, (expr))
        
        else:
            print ("Can not find any component in this file.")



    def create_testbench(self, component, port):
        '''
        This function create a testbench 
        '''
        for comp_name, comp_expr in self.component.iteritems():
            self.tb = io.StringIO()
            self.tb.write(u'''
-- This testbench is automatically generated using a python
-- script.
-- (c) Dilawar Singh, dilawar@ee.iitb.ac.in
--
library ieee;
use ieee.std_logic_1164.all;
use std.textio.all;
use work.all;

entity testbench is 
end entity testbench;

architecture stimulus of testbench is\n\tcomponent ''')
            self.tb.write(unicode(comp_name)+u'\n')
            self.tb.write(u'\tport ( \n')
            self.tb.write(u'\t'+unicode(comp_expr)+u'\n')
            self.tb.write(u'\t);\n')

            # Attach signal.
            for (name,comp), (a, expr) in self.port.iteritems():
                if comp == comp_name :
                    self.tb.write(u'\tsignal '+unicode(name)+u' : '+unicode(expr))
                    self.tb.write(u';\n')
                else:
                    pass

            self.tb.write(u'begin\n')
            self.tb.write(u'\tdut : '+unicode(comp_name)+u' \n\tport map (');

            for (name, comp), (a, expr) in self.port.iteritems():
                if comp == comp_name :
                    self.tb.write(unicode(name)+u', ')
                else:
                    pass
        
            
            pos = self.tb.tell()
            self.tb.seek(pos-2)
            self.tb.write(u' );')
            self.tb.write(u'\ttest : process \n')


            print self.tb.getvalue()


