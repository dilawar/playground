
"""
    moodle.py
    Author : Dilawar Singh
    Institute : IIT Bombay
    Email : dilawar@ee.iitb.ac.in
    Log : Created on Feb 16, 2012

    ABOUT : This module fetch assignements from moodle course page as specified
    in its configuration file .moodlerc which must be located in user home
    folder. See this file for options.

                                       
"""

import os
from iitb_moodle import IitbMoodle
from lang_vhdl import VHDL
from compare import CompareProgram
from create_graph import CreateNetwork

try:
    moodle = IitbMoodle()
    moodle.read_configuration()

except IOError as (errorno, strerror):
    print "I/O error({0}): {1}".format(errorno, strerror)

else :
    moodle.make_connection()
    moodle.get_course_page()
    moodle.download_data()
    print 'Total {0} assignments have been downloaded to {1}'.format(moodle.num_assignment, moodle.root_dir)
    
    lang = VHDL()
    lang.dirName(moodle.root_dir)
    
    if moodle.autotest == 'true' :
        lang.autotest = 'true'
    else:
        lang.autotest = 'false'

    if moodle.compile == 'true' :
        lang.compile = 'true'
    else :
        lang.compile = 'false'

    if moodle.compile == 'true' :
        print 'Compile flag is set.'
        if os.path.exists(lang.srcDir) :
            for x in os.walk(lang.srcDir):
                lang.compile_testbench(x[0], moodle.cxx)
        else:
            print "Given path does not exists."
    else:
        print 'Not compiling anything ..'

    if moodle.compare == 'true' :

        ''' 
        We need to iterate over moodle downloaded activities and check for
        similarity.
        '''
        print moodle.root_dir
        for i in moodle.activities :
            cmp = CompareProgram()
            cmp.set_dir_path(moodle.root_dir+"/"+i)
            #cmp.create_dict_of_program()
            cmp.traverse_and_compare()
            network = CreateNetwork()
