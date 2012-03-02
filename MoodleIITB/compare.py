''' 

This file read vhdl files in all directory and compare them and create a log
file which can be used by other script to analyze.

'''
import os, re, glob, difflib, sys
import collections as cl
import shutil
 
class CompareProgram():
    def __init__(self):
        self.dir_path = '.'
        self.allfiles = []
        self.file_dict = cl.defaultdict(list)
        self.lang = 'vhdl'
        self.log_name = "stats.log"
        self.log_name_low = "copy_low.log"
        self.log_name_med = "copy_medium.log"
        self.log_name_hig = "copy_high.log"




    def safe_backup(self, path, keep_original=True):
        """
        Rename a file or directory safely without overwriting an existing 
        backup of the same name.
        """
        count = -1
        new_path = path
        while True:
            if os.path.exists(path):
                if count == -1:
                    new_path = unicode("{0}.bak".format(path))
                else:
                    new_path = unicode("{0}.bak.{1}".format(path, count))
                if os.path.exists(new_path):
                    count += 1
                    continue
                else:
                    if keep_original:
                        if os.path.isfile(path):
                            shutil.copy(path, new_path)
                        elif os.path.isdir(path):
                            shutil.copytree(path, new_path)
                    else:
                        shutil.move(path, new_path)
                    break
            else:
                break
        return new_path


    def get_all_programs(self) :
        for dirpath, dirnames, filenames in os.walk(self.dir_path) :
            for file in filenames :
                if self.lang == 'vhdl' :
                    if re.search(r'\w+\.vhd[l]?', file):
                            path = dirpath+"/"+file
                            size = os.path.getsize(path)
                            if size > 2 :
                                self.allfiles.append(path)

    def create_dict_of_program(self):
        ''' Extract students names and create a map which keeps their files. '''
        index = 0
        prevKey = ''
        for i in self.allfiles:
            key = i.split('/')[2]
            if prevKey == key : 
                self.file_dict[(key, index)].append(i)
            else :
                self.file_dict[(key, index+1)].append(i)
                index = index + 1
                prevKey = key

    def init_log_file(self):
        log_path = self.safe_backup(self.log_name)
        self.log_file = open(log_path, 'a+')        
        log_path = self.safe_backup(self.log_name_low)
        self.log_file_low = open(log_path, 'a+')
        log_path = self.safe_backup(self.log_name_med)
        self.log_file_med = open(log_path, 'a+')
        log_path = self.safe_backup(self.log_name_hig)
        self.log_file_hig = open(log_path, 'a+')


  
    def create_log_file(self) :
        self.init_log_file()
        self.get_all_programs()
        self.create_dict_of_program()
        count = 0
        for k in self.file_dict :
            name1, id1 = k
            print 'Checking for {0}'.format(name1)
            for fl1 in self.file_dict[k] :
                with open(fl1, 'r') as f1 :
                    text1 = f1.read()
                    for l in self.file_dict :
                        name2, id2 = l
                        if id2  <= id1  : pass
                        else:
                            for fl2 in self.file_dict[l] :
                               count = count + 1
                               with open(fl2, 'r') as f2 :
                                  text2 = f2.read()
                                  if len(text1) < 10 : pass
                                  if len(text2) < 10 : pass

                                  s = difflib.SequenceMatcher(None,\
                                          text1.lower(), text2.lower())
                                  lst = s.get_matching_blocks()
                                  w = 0
                                  for a, b, n in lst :
                                      w = w + len(lst)*n
                                  
                                  log = '{0}, {1}, {2}, {3}, {4}, {5} \n'.format(\
                                       count , w, w/len(lst) ,s.ratio(), f1.name, f2.name )
                                  # there is no use of w < 100 file.
                                  if w > 100 :
                                      self.log_file.write(log)
                                  
                                  if s.ratio() > 0.2 and s.ratio() < 0.4  :
                                      print 'Mild copying possible in files'
                                      print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                                      self.log_file_low.write(log)
                                  if s.ratio() > 0.4 and s.ratio() < 0.55  :
                                      print 'Significant copying possible in files'
                                      print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                                      self.log_file_med.write(log)
                                  if s.ratio() > 0.55  :
                                      print 'These two files are alomost copied.'
                                      print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)
                                      self.log_file_hig.write(log)

                            
# Let's get down to business.
plag = CompareProgram()
plag.create_log_file()
