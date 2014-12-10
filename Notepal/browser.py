"""
    browser.py
    Author : Dilawar Singh
    Institute : IIT Bombay
    Email : dilawar@ee.iitb.ac.in
    Log : Created on Feb 16, 2012

    ABOUT : This module fetch assignements from moodle course page as specified
    in its configuration file .moodlerc which must be located in user home
    folder. See this file for options.

                                       
"""

import os
import re
import mechanize, urllib, urllib2
import sys, os, shutil, getpass, glob, subprocess

class Browser():

    """ A python application to access moodle and download data from it.
    """
    def __init__(self):
        print("Initializing browser ... ")
        self.proxy = False
        self.br = mechanize.Browser( factory=mechanize.RobustFactory())
        self.br.set_handle_equiv(False)
        self.br.set_handle_robots(False)
        self.br.set_handle_referer(False)
        self.br.set_handle_redirect(True)
        self.br.set_debug_redirects(True)
        self.br.set_debug_responses(False)
        self.br.set_debug_http(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=2)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux 1686; en-US;\
            rv:1.9.0.1) Gecko/201171615 Ubuntu/11.10-1 Firefox/3.0.1')]
    
    def set_proxy(self, proxy=None):
        if not proxy:
            self.br.set_proxies({})
        else:
            self.br.set_proxies({"http": os.environ['http_proxy']
                , "ftp": os.environ['ftp_proxy']
                , "https" : os.environ['https_proxy']}
                )

    def read_configuration(self):
        """ This function reads a config file and set the values needed for
        making a successfull connection to Moodle.
        """
        print("Reading configuration file ...")
        self.url = 'https://doqcs.ncbs.res.in/notepal2013'
        self.username = "dilawars"
        self.password = ""
        home = os.environ['HOME']
        path = home+"/.notepalrc"
        if os.path.isfile(path) :
            f = open(path, 'r')
        else :
            print("File .notepalrc does not exists in your home folder."
                    " Existing..."
                    )
            sys.exit(0)

        for line in f :
            if line[0] == '#' :
                pass

            elif line.split() == "" :
                pass
            
            else :
                (key, val) = line.split("=")

                if key.split()[0] == 'url' :
                    self.url = val.split()[0]
                
                elif key.split()[0] == 'username' :
                    self.username = val.split()[0]

                elif key.split()[0] == 'password' :
                    self.password = ' '.join(val.split())
                    if self.password == '':
                        self.password=getpass.getpass()
                else :
                     print("Unknow configuration variable {0}.  Ignoring.".format(key.split()[0]))


    def make_connection(self):
        if self.proxy != "false" :
            print("Using proxy variables from environment ...")
        else :
            print("Ignoring proxy variables...")
            self.set_proxy()

        print("Logging into notepal : {}".format(self.url))
        res = self.br.open(self.url)

        # select the form and login
        assert self.br.viewing_html()

        form_id = 0;
        for i in self.br.forms():
            id = i.attrs.get('id') 
            id = id.lower()
            if id.find("login") == 0 :
                #select form 1 which is used for login.
                assert self.username.strip()
                assert self.password.strip()
                self.br.select_form(nr = form_id)
                print self.br.forms
                self.br.form['username'] = self.username.strip()
                self.br.form['password'] = self.password.strip()
                res = self.br.submit()
                res = self.br.response()
            else:
                form_id = form_id + 1;

