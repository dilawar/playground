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

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
print("[INFO] Firefox Headless Browser Invoked")
import time

downloadBtnID = 'ctl00_ctl00_dpPH_dpPH_btnSearch'
tableId = 'ctl00_ctl00_dpPH_dpPH_gdCALs'
states_ = []

def find_select_by_id( id ):
    global driver
    ss = driver.find_element_by_id( id )
    return Select(ss)

def download_kmp( state, siteType):
    global driver
    global states_
    driver.get( baseUrl_ )
    ss = find_select_by_id( "ctl00_ctl00_dpPH_dpPH_ddlState")
    states_ = [ o.text for o in ss.options ][1:]
    ss.select_by_visible_text( state )

    ss = find_select_by_id( 'ctl00_ctl00_dpPH_dpPH_ddlSiteType' )
    caTypes_ = [ o.text for o in ss.options ][1:]
    print( caTypes_ )
    ss.select_by_visible_text( siteType )

    submit = driver.find_element_by_id( 'ctl00_ctl00_dpPH_dpPH_btnSearch')
    submit.click()
    time.sleep(1)

    # now download verything on this page.
    trs = driver.find_elements_by_xpath( '//table[@id="%s"]//tr' % tableId )
    for i, tr in enumerate(trs):
        #  print( i, tr.get_attribute( 'innerHTML') )
        d = tr.find_element_by_xpath( '//input[@text="Download"]' )
        print( i, d )
        d.click()

def main( ):
    global driver
    state = sys.argv[1]
    siteType = sys.argv[2]
    print( '[INFO]  State: %s, Site Type: %s' % (state, siteType))
    try:
        download_kmp( state, siteType)
    except Exception as e:
        print( e )
        driver.quit()

    driver.quit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print( 'CTRL+C' )
        driver.quit()
