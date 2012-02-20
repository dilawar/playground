import re
import glob, os, subprocess

class VHDL:

    def __init__(self):
        self.test_bench = ''
        self.src = ''
        self.srcDir = ''

    def dirName(self, dir):
        self.srcDir = dir

    def compile_testbench(self, dir):
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
                        #print("Testbench entity is {0}".format(test_bench))
                        #print("In file {0}".format(f.name))
                        vcdOption = "--vcd="+test_bench+".vcd"
                        subprocess.call(["ghdl", "-a", f.name])
                        subprocess.call(["ghdl", "-m", test_bench])
                        subprocess.call(["ghdl", "-r", test_bench, "--stop-time=1000ns", \
                            vcdOption])

                    else : 
                        #print "No testbench."
                        pass
'''
vhdl = VHDL()
vhdl.dirName('/home/dilawar/Works/myrepo/Courses/2012_VLSIDesignLab/Lab session 1')
print vhdl.srcDir
if os.path.exists(vhdl.srcDir) :
    for x in os.walk(vhdl.srcDir):
        vhdl.compile_testbench(x[0])
else:
    print "Given path does not exists."
'''
