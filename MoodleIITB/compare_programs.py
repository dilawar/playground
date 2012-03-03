''' 

This file read vhdl files in all directory and compare them and create a log
file which can be used by other script to analyze.

'''
import os, re, difflib
import sys
import time
import collections as cl
import shutil
import cStringIO
from IPython import embed
 
class CompareProgram():
    def __init__(self):
        self.src_path = '.'
        self.log_dir = self.src_path+"/stats/"
        self.allfiles = []
        self.file_dict = cl.defaultdict(list)
        self.total_program = 0
        self.lang = 'vhdl'
        self.log_name = self.src_path+"/stats.log"
        self.log_name_low = self.src_path+"/copy_low.log"
        self.log_name_med = self.src_path+"/copy_medium.log"
        self.log_name_hig = self.src_path+"/copy_high.log"
        self.is_log = True

    
    
    def set_dir_path(self, dir, delFlag):
        
        if os.path.exists(dir):
            stat_dir = dir+"/stats"
            if os.path.exists(stat_dir):
                if delFlag == True :
                    # create a backup with timestamp.
                    shutil.copytree(stat_dir, stat_dir+'_'+unicode(time.time()))
                    shutil.rmtree(dir+"/stats")
                    os.makedirs(dir+"/stats")
                else : pass
            else:
                os.makedirs(dir+"/stats")
        else : 
            print 'There is no dirctory {0}'.format(dir)
            sys.exit(0)

        self.src_path = dir
        self.log_dir = self.src_path+"/stats/"
        self.log_name = self.log_dir+"/stats.log"
        self.log_name_low = self.log_dir+"/copy_low.log"
        self.log_name_med = self.log_dir+"/copy_medium.log"
        self.log_name_hig = self.log_dir+"/copy_high.log"


    def safe_backup(self, path, keep_original=True):
        
        """safe_backup

        Rename a file or directory safely without overwriting an existing 
        backup of the same name.
        
        """
        count = -1
        new_path = path
        while True:
            if os.path.exists(path):
                new_path = unicode("{0}.bak".format(path))
                if os.path.isfile(path):
                        shutil.copy(path, new_path)
                elif os.path.isdir(path):
                        shutil.copytree(path, new_path)
                else:
                    shutil.move(path, new_path)
                break
            else:
                break
        return path


    def get_all_programs(self) :
        count = 0;
        for dirpath, dirnames, filenames in os.walk(self.src_path) :
            for file in filenames :
                if self.lang == 'vhdl' :
                    if re.search(r'\w+\.vhd[l]?$', file):
                            path = dirpath+"/"+file
                            size = os.path.getsize(path)
                            if size > 2 :
                                self.allfiles.append(path)
                                count = count + 1
        self.total_program = count
        print "Total {0} programs".format(self.total_program)

    def create_dict_of_program(self):
        
        '''create_dict_of_program
        
        Extract students names and create a map which keeps their files. 
        
        '''
        
        self.get_all_programs()
        index = 0
        prevKey = ''
        for i in self.allfiles:
            key = i.split(self.src_path)[1]
            key = key.split('/')[1]
            if prevKey == key : 
                self.file_dict[(index, key)].append(i)
            else :
                self.file_dict[(index+1, key)].append(i)
                index = index + 1
                prevKey = key

        

    def init_log_streams(self):
        # string streams.
        self.log_file = cStringIO.StringIO()
        self.log_file_low = cStringIO.StringIO()
        self.log_file_med = cStringIO.StringIO()
        self.log_file_hig = cStringIO.StringIO()


    def compare_with_programs(self, count,  file, dict):
        #print ' Compare with {0}'.format(file)
        #print dict
        with open(file, 'r') as f1 :
            for i in dict :
                with open(i, 'r') as f2:
                    text1 = f1.read()
                    text2 = f2.read()

                    if len(text1) < 10 : pass
                    if len(text2) < 10 : pass
                    s = difflib.SequenceMatcher(None, text1.lower(), text2.lower())
                    lst = s.get_matching_blocks()
                    w = 0
                    for a, b, n in lst :
                        w = w + len(lst)*n
    
                    log = '{0}, {1}, {2}, {3}, {4}, {5} \n'.format(\
                            count , w, w/len(lst) ,s.ratio(), f1.name, f2.name )
                    # there is no use of w < 100 file.
                    if w > 100 :
                        self.log_file.write(log)
    
                    if s.ratio() > 0.17 and s.ratio() < 0.35  :
                        print 'Mild copying possible in files'
                        print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                        self.log_file_low.write(log)
                    if s.ratio() > 0.35 and s.ratio() < 0.50  :
                        print 'Significant copying possible in files'
                        print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                        self.log_file_med.write(log)
                    if s.ratio() >= 0.50  :
                        print 'These two files matches a lot!'
                        print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                        self.log_file_hig.write(log)
                    else : pass
                        #print 'No significant match.'
                        #print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
    

    def save_logs(self):
        log_path = (self.log_name)
        with open(log_path, 'w') as log_file_f :
            log_file_f.write(self.log_file.getvalue())

        log_path =(self.log_name_low)
        with  open(log_path, 'w') as  log_file_low_f :
            log_file_low_f.write(self.log_file_low.getvalue())

        log_path = (self.log_name_med)
        with  open(log_path, 'w') as  log_file_med_f :
            log_file_med_f.write(self.log_file_med.getvalue())

        log_path = (self.log_name_hig)
        with  open(log_path, 'w') as log_file_hig_f :
            log_file_hig_f.write(self.log_file_hig.getvalue())



    def traverse_and_compare(self):
        self.init_log_streams()
        self.create_dict_of_program()
        cnt0 = 0
        comp = dict()
        for i in self.file_dict :
            id1, name1 = i
            cnt1 = 0
            print 'Comparing for {0}'.format(name1)
            for fl1 in self.file_dict[i]:
                lst = []
                for j in self.file_dict :
                    id2, name2 = j
                    if j <= i : pass
                    else :
                        lst.append(id2)
                        cnt1 = cnt1 + len(self.file_dict[j])
                        #print 'X', fl1, self.file_dict[j]
                        self.compare_with_programs(cnt0, fl1, self.file_dict[j])
                comp[id1] = lst
                #print 'For {0}, total {1} comparison'.format(fl1, cnt1)
                cnt0 = cnt0 + cnt1
        #print 'Total comparisions {0}'.format(cnt0)
        self.save_logs()   
