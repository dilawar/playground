import re
import glob, os, subprocess, sys

class VHDL:

    def __init__(self):
        self.test_bench = ''
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
                while True:
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
                (\s*\w+(\s*[,]\s*\w+\s*)*\s*[:]\s*
                (in|out)\s*\w+\s*([(]\s*\d+\s*\w+\s*\d+\s*[)])*\s*[;]*)*
                \s*[)]\s*[;]
                \s+end\s+component\s*\w*[;]'''
                , data, re.I | re.VERBOSE)

        if m:
            print m.group(0)
            print m.group(1)
            print m.group(2)
        
        else:
            print ("Can not find any component in this file.")
            os.system("pause")


