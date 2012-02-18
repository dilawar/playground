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

else :
    moodle.make_connection()
    moodle.get_course_page()
    moodle.download_data()
    print 'Total {0} assignments have been downloaded to {1}'.format(moodle.num_assignment, moodle.root_dir)
