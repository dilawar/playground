import smtplib
import mimetypes
from optparse import OptionParser
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import formatdate
from email import Encoders

class SendEmails():

    def __init__(self, dir, activity_name):
        self.log_path = dir
        self.log_list = []
        self.activity = unicode(activity_name)
        self.student_dict = cl.defaultdict(list)
        self.src_path = dir.split('stats')[0]
        self.down_dir = dir.split(activity_name)[0]
 

    def send_emails(self, convict_dict, accused_dict):

        '''
        This function sends email to student who should meet the instructors.
        '''
        print 'Getting emails database. Make sure you have grades.txt (CSV) file your'
        print '{0}'.format(self.src_path)

        if os.path.exists(self.down_dir+"/grades.txt") :
            fl_grader = open(self.down_dir+"/grades.txt", "r")
        else :
            print 'File grades.txt (CSV) does not exists in {0}'\
                    .format(self.down_dir)
            sys.exit(32)
        
        # create data_base of emails and marks. 
        dict_students = cl.defaultdict(list)
        # ignore the first line.
        first_line = fl_grader.readline()
        for line in fl_grader.readlines() :
            ln = line.split(',')
            if ln[1] == '': # if surname is not present.
                key = ln[0]
            else : # append surname.
                key = ln[0]+' '+ln[1]

            dict_students[key] = ln[2:] 

        for i in convict_dict : 
            tarfile_name = self.log_path+'/'+'_'.join(self.activity.split())\
                    +'_'+'_'.join(i.split())+'.tar'
            email_id = dict_students[i]
            msg = ''
            #print tarfile_name
            with tarfile.open(tarfile_name, 'w:gz') as tar :
                for entry in  convict_dict[i] :
                    # create an archive.
                    file1 = entry[0]
                    file2 = entry[1]
                    msg = '\n\n |- {0}\n |- {1}\n |- MATCH INDEX {2}'\
                            .format(file1, file2, entry[2])
                    tar.add(self.src_path+file1, recursive=False, arcname=file1)
                    tar.add(self.src_path+file2, recursive=False, arcname=file2)
            tar.close()

            # Now construct the mail msg
            HOST = 'smtp-auth.iitb.ac.in'
            message = MIMEMultipart()
            FROM = 'dilawars@iitb.ac.in'
            TO = 'dilawar.rajput@gmail.com'
            message["From"] = "dilawars@iitb.ac.in"
            message["To"] = "dilawar.rajput@gmail.com"
            message["Subject"] = "Attached files are very similar. Meet your instructor!"
            message["Date"] = formatdate(localtime=True)

            text = 'Hi,'\
                    +'You are enrolled in EE 705 and have submitted these attached'\
                    +'\nfiles.'\
                    +'\n\n'\
                    +'These files are found to be very similar with other files.' \
                    +'\nThey are also included in attachment for your reference' \
                    +'\nYour grades have been blocked! Please meet your instructor.'\
                    +'\n--\n' \
                    +'\nThis email is system-generated. You need not reply.' \
                    +'\nIf attached files do not match each other, kindly reply back.'

            text = text + msg 
            message.attach(text)
            # attach a file
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(tarfile_name,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                    % os.path.basename(tarfile_name))
            message.attach(part)
         
            # get username and password.
            username = os.getenv('proxy_username')
            password = os.getenv('proxy_password')

            server = smtplib.SMTP(HOST, 25)
            server.starttls()
            server.set_debuglevel(1)
            server.login(username, password)  # optional
            try:
                failed = server.sendmail(FROM, TO, message.as_string())
                server.close()
            except Exception, e:
                errorMsg = "Unable to send email. Error: %s" % str(e)  
             
