from graph_tool.all import *
import collections as cl
import pickle
import os
import pylab as pl
import cStringIO
import tarfile
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


class NetworkPrograms():

    def __init__(self, dir, activity_name):
        self.log_path = dir
        self.log_list = []
        self.activity = unicode(activity_name)
        self.student_dict = cl.defaultdict(list)
        self.src_path = dir.split('stats')[0]
        self.down_dir = dir.split(activity_name)[0]
        
    def init_log_list(self):
        with open(self.log_path+"/log_list.pkl", 'rb') as lst :
            self.log_list = pickle.load(lst)

    
    def shorten_file_name(self, file_name):
        return file_name.split(self.src_path)[1]
    
    def get_student_name(self, file_name):
        file_name_short = self.shorten_file_name(file_name)
        return file_name_short.split('/')[0]
    
    def create_student_dict(self):
        for entry in self.log_list :
            student1 = self.get_student_name(entry[0])
            student2 = self.get_student_name(entry[1])
            if student1 in self.student_dict : pass
            else :
                self.student_dict[student1] = len(self.student_dict) + 1
            
            if student2 in self.student_dict : pass
            else :
                self.student_dict[student2] = len(self.student_dict) + 1

    def create_network(self):
        self.init_log_list()
        self.create_student_dict()
        
        # initialize graph.
        self.g = Graph(directed = False)
        v_name = self.g.new_vertex_property("string")
        e_filepair = self.g.new_edge_property("object")
        e_similarity_index = self.g.new_edge_property("double")
        e_matched_blocks = self.g.new_edge_property("int")
        e_average_match = self.g.new_edge_property("int")
        e_file_size_ratio = self.g.new_edge_property("double")
        e_edge_width = self.g.new_edge_property("double")

        # Add vertices to it.
        v_dict = dict() # to keep the index of vertices.
        for entry in self.student_dict :
            v = self.g.add_vertex()
            v_name[v] = entry
            v_dict[entry] = v

        # and now add edges to it.
        for entry in self.log_list :
            src = self.get_student_name(entry[0])
            tgt = self.get_student_name(entry[1])

            file_pair = [self.shorten_file_name(entry[0])\
                    , self.shorten_file_name(entry[1])]

            similariry_index = entry[2]
            file_size_ratio = entry[3]
            matched_blocks = entry[4]
            average_match = entry[5]

            e = self.g.add_edge(v_dict[src], v_dict[tgt])
            
            # attache properties to edges.
            e_filepair[e] = file_pair
            e_similarity_index[e] = similariry_index
            e_edge_width[e] = pow(2*similariry_index, 2)
            e_file_size_ratio[e] = file_size_ratio
            e_matched_blocks[e] = matched_blocks
            e_average_match[e] = average_match
            

        # Attach edges and vertex properties to graph.
        self.g.edge_properties["e_similarity_index"] = e_similarity_index
        self.g.edge_properties["e_file_pair"] = e_filepair
        self.g.edge_properties["e_matched_blocks"] = e_matched_blocks
        self.g.edge_properties["e_average_match"] = e_average_match
        self.g.edge_properties["e_file_size_ratio"] = e_file_size_ratio
        self.g.edge_properties["e_edge_width"] = e_edge_width
        self.g.vertex_properties["v_name"] = v_name

        # Let's save this graph for posterity.
        self.g.save(self.log_path+"/full_graph.xml.gz")

        return v_dict, self.g


    def generate_plagiarism_graph(self):

        if not os.path.exists(self.log_path+"/full_graph.xml.gz"):
                v_dict, g = self.create_network()
        else :
            g = load_graph(self.log_path+"/full_graph.xml.gz")
            
        print 'Finding out highly mathcing content.'
        e_similarity_index = g.edge_properties["e_similarity_index"]
        e_pen_width = g.edge_properties["e_edge_width"]
        e_file_size_ratio = g.edge_properties["e_file_size_ratio"]

        g1 = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.60 \
                )

        graph_draw(g1 \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index \
                , size = (100,100) \
                , sep = 2 \
                , penwidth = e_pen_width \
                , vsize = 0.05 \
                , output = self.log_path+"/copy_high.png" \
                )
        
        g2 = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.48 \
                )

        graph_draw(g2 \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index \
                , size = (100,100) \
                , sep = 2 \
                , penwidth = e_pen_width \
                , vsize = 0.05 \
                , output = self.log_path+"/copy_suspect.png" \
                )

        g3 = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.35 \
                )

        graph_draw(g3 \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index
                , size = (100,100)
                , sep = 2 \
                , penwidth = e_pen_width \
                , vsize = 0.05 \
                , output = self.log_path+"/copy_all.png" \
                )
        
        g_all = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.23 \
                and e_file_size_ratio[e] > 0.2 and e_file_size_ratio[e] < 4 \
                )

        #pos = fruchterman_reingold_layout(g_all, n_iter = 1000)
        #pos = random_layout(g_all)
        graph_draw(g_all \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index
                , size = (100,100)
                , sep = 5 \
                #, pos = pos
                , penwidth = e_pen_width
                , vsize = 0.05
                , output = self.log_path+"/detailed.png" \
                )

    def create_msg_dictionaries(self):

        msg = cStringIO.StringIO()
        full_copy_dict = cl.defaultdict(list)
        possible_copy_dict = cl.defaultdict(list)
        
        # get the graph.
        if not os.path.exists(self.log_path+"/full_graph.xml.gz"):
                v_dict, g = self.create_network()
        else :
            g = load_graph(self.log_path+"/full_graph.xml.gz")
        
        e_similarity_index = g.edge_properties["e_similarity_index"]
        e_file_size_ratio = g.edge_properties["e_file_size_ratio"]
        e_file_pair = g.edge_properties["e_file_pair"]
        v_name = g.vertex_properties["v_name"]

        print 'Finding out highly mathcing content.'
        
        for edge in g.edges() :
             if e_file_size_ratio[edge] > 0.25 and e_file_size_ratio[edge] < 4:
                if e_similarity_index[edge] > 0.63 :
                    src, tgt =  edge
                    st1 = v_name[src]
                    st2 = v_name[tgt]
                    pair = e_file_pair[edge]
                    match = [pair[0], pair[1], e_similarity_index[edge]]
                    full_copy_dict[st1].append(match)
                    full_copy_dict[st2].append(match)

                elif e_similarity_index[edge] >= 0.50 :
                    src, tgt =  edge
                    st1 = v_name[src]
                    st2 = v_name[tgt]
                    pair = e_file_pair[edge]
                    match = [pair[0], pair[1], e_similarity_index[edge]]
                    possible_copy_dict[st1].append(match)
                    possible_copy_dict[st2].append(match)
                else : pass

                # if there are more than one file with 0.5 matching, send it to
                # full_copy_dict
                to_del = []
                for i in possible_copy_dict :
                    if len(possible_copy_dict[i]) >= 2 :
                        for line in possible_copy_dict[i] :
                            full_copy_dict[i].append(line)
                        # remove this entry from possible copy.
                        to_del.append(i)
                    else : pass
                
                for i in to_del :
                    del(possible_copy_dict[i])

        # save a log file.
        f = cStringIO.StringIO()
        f.write("Following stundents have copied.\n\n")
        for i in full_copy_dict :
            f.write('\n:'+unicode(i)+":\n")
            for line in full_copy_dict[i] :
                f.write("|-"+unicode(line[0])+'\n|-'+unicode(line[1])\
                        +'\n** Matching : '+unicode(line[2])+'\n')

        with open(self.log_path+"/"+self.activity+"_convicted.txt", "w") as fl :
            fl.write(f.getvalue())
        
        f = cStringIO.StringIO()
        f.write("\n\nFollowing students may have copied. Verify manually\n")
        for i in possible_copy_dict :
            f.write('\n:'+unicode(i)+":\n")
            for line in possible_copy_dict[i] :
                f.write("|-"+unicode(line[0])+'\n|-'+unicode(line[1])\
                        +'\n** Matching : '+unicode(line[2])+'\n')

        with open(self.log_path+"/"+self.activity+"_accused.txt", "w") as fl :
            fl.write(f.getvalue())

        return full_copy_dict, possible_copy_dict

    def send_emails(self):

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

        print 'Generating emails to be sent.'
        convict_dict, accused_dict = self.create_msg_dictionaries()

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
             
