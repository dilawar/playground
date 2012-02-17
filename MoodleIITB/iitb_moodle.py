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
import re
import mechanize, urllib, urllib2
import cookielib, logging, html2text
import sys, os, shutil

class IitbMoodle():

    """ A python application to access moodle and download data from it.
    """
    def __init__(self):
        print("Initializing link ... ")
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
        self.enable_logging(False);
    
    def set_proxy(self):
        self.br.set_proxies({})


    def enable_logging(self, log_flag):
        if log_flag == True :
            logger = logging.getLogger("mechanize")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)
        else:
            pass

    def read_configuration(self):
        """ This function reads a config file and set the values needed for
        making a successfull connection to Moodle.
        """
        print("Reading configuration file ...")
        self.url = 'http://moodle.iitb.ac.in/login/index.php'
        self.username = ""
        self.password = ""
        self.course_key = ""
        self.activity_name = ""
        self.activities = []
        self.num_assignment = 0;
        self.root_dir = "./Moodle";
        self.proxy = "false"
        home = os.environ['HOME']
        path = home+"/.moodlerc"
        if os.path.isfile(path) :
            f = open(path, 'r')
        else :
            print "File .moodlerc does not exists in your home folder. \
            Existing..."
            sys.exit(0)

        for line in f :
            
            if line[0] == '#' :
                pass

            elif line.split() == "" :
                pass
            
            else :
                (key, val) = line.split("=")
                if key.split()[0] == 'username' :
                    self.username = val.split()[0]
                
                elif key.split()[0] == 'password' :
                    self.password = val.split()[0]

                elif key.split()[0] == 'course' :
                    val = ' '.join(val.split())
                    self.course_key = val
                

                elif key.split()[0] == 'activities' :
                    val = ' '.join(val.split())
                    self.activity_name = val

                elif key.split()[0] == 'activity' :
                   val = ' '.join(val.split())
                   self.activities.append(val)
                
                elif key.split()[0] == 'download' :
                   self.root_dir = val.split()[0]
                
                elif key.split()[0] == 'proxy' :
                   self.proxy = val.split()[0]

                else :
                     print ("Unknow configuration variable.. Ignoring.")


    def make_connection(self):
        if self.proxy == "true" :
            print("Acquiring proxy variables from environment ...")
        else :
            print("Ignoring proxy variables...")
            self.set_proxy()

        print("Logging into Moodle ..")
        res = self.br.open(self.url)
        # select the form and login
        assert self.br.viewing_html()

        form_id = 0;
        for i in self.br.forms():
            id = i.attrs.get('id') 
            id = id.lower()
            if id.find("login") == 0 :
                #select form 1 which is used for login.
                self.br.select_form(nr = form_id)
                self.br.form['username'] = self.username
                self.br.form['password'] = self.password
                self.br.submit()
                print(" |- Submitting login form ...")
                res = self.br.response()
                res_html = res.get_data()
                #print html2text.html2text(res_html)
            else:
                form_id = form_id + 1;

    def get_course_page(self):

        self.course = self.br.follow_link(text_regex=self.course_key)
        course_url = self.course.geturl()
        [url, id ] = course_url.split('id=')
        self.course_id = id
        print(" |- Acquiring course id ...")

        #course_html = self.course.get_data()
        #print html2text.html2text(course_html)

    def goto_main_activity(self):
        self.activity_id = []
        print (" |- Acquiring link of activity ... ")
        print self.activity_name
        activity_res = self.br.follow_link(text_regex=self.activity_name)
        for act in self.activities :
            act_res = self.br.follow_link(text_regex=act)
            act_url = act_res.geturl()
            [url, act_id] = act_url.split('id=')
            self.activity_id.append(act_id)

            view_act_res = self.br.follow_link(text_regex=r".*(View).*[0-9]*(submitted).*")
            self.fetch_activity_links(view_act_res)
            self.download_files(act)
            print("****")
            print("Successfully downloaded data for this activity. Iterating over activities ...")
            self.br.open(activity_res.geturl())

    def fetch_activity_links(self, link_res):
        self.user_dict = dict()
        """ Fetch user_id from the links. """
        for link in self.br.links(url_regex="course="+self.course_id):
            user_url = link.url
            [url, user_course_id] = user_url.split("id=")
            [user_id, rest] = user_course_id.split("&course")
            self.user_dict[user_id] = [link.text,""]

        """ For each user, fetch its assignement, if submitted. """
        for user in self.user_dict.keys():
            for link in self.br.links(url_regex=user):
                file_format = ['.tar', '.gz', '.zip', '.rar', '.7z', '.bz']
                found = False;
                for format in file_format:
                    if link.url.endswith(format) == True:
                        found = True
                        ''' Only update the url. '''
                        self.user_dict[user][1] =  link.url
                        self.num_assignment = self.num_assignment + 1

                    else:
                        found = False

    
    def download_data(self) :
        self.dir = "./Moodle"
        self.goto_main_activity()

    def download_files(self, act) :
        down_dir = self.root_dir +"/"+act
        if not os.path.exists(down_dir) :
            os.makedirs(down_dir)
        print(" |- Setting download directory to " + down_dir)
        for user in self.user_dict.keys() :
            if self.user_dict[user] == "":
                pass
            else :
                url = self.user_dict[user][1]
                if url == '':
                    pass
                else:
                    temp_dir = down_dir+"/"+self.user_dict[user][0]
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)

                    print(" * Downloading submission of  "+self.user_dict[user][0])
                    loc = self.br.retrieve(url)[0]
                    shutil.move(loc,temp_dir) 

