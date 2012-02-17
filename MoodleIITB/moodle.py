from iitb_moodle import IitbMoodle

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

try:
    moodle = IitbMoodle()
    moodle.read_configuration()

except IOError as (errorno, strerror):
    print "I/O error({0}): {1}".format(errorno, strerror)

except moodle.proxy_exception:
    print("Error: Configuration file error! File name ~/.moodlerc")

else :
    moodle.make_connection()
    moodle.get_course_page()
    moodle.download_data()
    print ("Total ", moodle.num_assignment, "assignments have been downloaded to ", \
         moodle.root_dir, "directory")

