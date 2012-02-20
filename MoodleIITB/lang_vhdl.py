import re
import glob, os

class VHDL:

    def __init__(self):
        self.test_bench = ''
        self.src = ''
        self.srcDir = ''

    def dirName(self, dir):
        self.srcDir = dir

    def search_testbench(self, dir):
        files = glob.glob(dir+'/*.vhd')
        for file in files:
                f = open(file, "r")
                while True:
                    try:
                        self.src = f.read()
                    except EOFError:
                        print "EOF"
                    if not self.src: break
                    # This will match the testbech entity in given file.
                    m = re.search(r"entity\ +(\w+)\ +is[\ \n]+end\ +(\w*)[;]", self.src, re.I)
                    if m : 
                        self.compile_testbench(m.group(1), f)
                    else : 
                        #print "No testbench."
                        pass

    def compile_testbench(self, test_bench, file):
        '''
        This function compiles the test_bench in given directory.
        
        '''
        print("Testbench entity is {0}".format(test_bench))
        print("In file {0}".format(file.name))


vhdl = VHDL()
vhdl.dirName('/home/dilawar/Works/myrepo/Courses/2012_VLSIDesignLab/Lab session 1')
print vhdl.srcDir
if os.path.exists(vhdl.srcDir) :
    for x in os.walk(vhdl.srcDir):
        vhdl.search_testbench(x[0])
else:
    print "Given path does not exists."

