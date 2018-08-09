#!/usr/bin/env python
"""download_all_kml.py: 
Download all kml file.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
baseUrl_ = 'http://egreenwatch.nic.in/Public/Reports/View_Download_KML.aspx'

import robobrowser
from requests import Session
session = Session()
session.verify = False
br_ = robobrowser.RoboBrowser( session = session, history = True )
#  import mechanicalsoup as ms
#  br_ = ms.StatefulBrowser()

def download_kmp( state, siteType):
    global br_
    br_.open( baseUrl_ )
    # get the form
    form = br_.get_form( action='./View_Download_KML.aspx' )
    try:
        form[ "ctl00$ctl00$dpPH$dpPH$ddlState"].value = state
        form[ "ctl00$ctl00$dpPH$dpPH$ddlSiteType"].value = siteType
    except Exception as e:
        print( 'One or more parameter are not correct')
        print( e )
        quit( 1 )

    # now submit.
    br_.submit_form( form )

    # now submit the form 
    form = br_.get_form( action='./View_Download_KML.aspx' )
    print( form.fields )
    print( form.serialize() )
    

def main( ):
    state = sys.argv[1]
    siteType = sys.argv[2]
    print( '[INFO]  State: %s, Site Type: %s' % (state, siteType))
    download_kmp( state, siteType)

if __name__ == '__main__':
    main()
