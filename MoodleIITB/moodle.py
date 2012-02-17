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
except moodle.Exception:
    print("Error: Configuration file error! File name ~/.moodlerc")

try :
    moodle.make_connection()
except moodle.Exception:
    print("Error: Failed to make connection!")

try :
    moodle.get_course_page()
except moodle.Exception:
    print("Error: Course page does not exists or incorrect regular expression.")

try :
    moodle.download_data()
    print ("Total ", moodle.num_assignment, "assignments have been downloaded to ", \
         moodle.root_dir, "directory")
except moodle.Exception:
    print("Error: Can not download data. Do you have enough priviledges.")

