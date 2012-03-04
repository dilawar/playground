from graph_tool.all import *
import collections as cl
import pickle
import pylab as pl
import cStringIO

class NetworkPrograms():

    def __init__(self, dir):
        self.log_path = dir
        self.log_list = []
        self.student_dict = cl.defaultdict(list)
        self.src_path = dir.split('stats')[0]
        
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

        v_dict, g = self.create_network()

        print 'Finding out highly mathcing content.'
        e_similarity_index = g.edge_properties["e_similarity_index"]
        e_pen_width = g.edge_properties["e_edge_width"]
        e_file_size_ratio = g.edge_properties["e_file_size_ratio"]

        g1 = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.60 \
                )

        graph_draw(g1 \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index
                , size = (100,100)
                , sep = 2 \
                , penwidth = e_pen_width
                , vsize = 0.05
                , output = self.log_path+"/copy_high.png" \
                )
        
        g2 = GraphView(g \
                , efilt= lambda e : e_similarity_index[e] > 0.48 \
                )

        graph_draw(g2 \
                #, vprops = {"label" :g.vertex_properties["v_name"]} \
                , ecolor = e_similarity_index
                , size = (100,100)
                , sep = 2 \
                , penwidth = e_pen_width
                , vsize = 0.05
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
                , penwidth = e_pen_width
                , vsize = 0.05
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
        v_dict, g = self.create_network()

        print 'Generating emails to be sent.'
        msg = cStringIO.StringIO()
        full_copy_dict = cl.defaultdict(list)
        possible_copy_dict = cl.defaultdict(list)
        
        # get the graph.
        v_dict, g = self.create_network()
        e_similarity_index = g.edge_properties["e_similarity_index"]
        e_file_size_ratio = g.edge_properties["e_file_size_ratio"]
        e_file_pair = g.edge_properties["e_file_pair"]
        v_name = g.vertex_properties["v_name"]

        print 'Finding out highly mathcing content.'
        
        for edge in g.edges() :
             if e_file_size_ratio[edge] > 0.25 and e_file_size_ratio[edge] < 4:
                if e_similarity_index[edge] > 0.60 :
                    src, tgt =  edge
                    st1 = v_name[src]
                    st2 = v_name[tgt]
                    pair = e_file_pair[edge]
                    match = '\n |-{0}\n |-{1}\n'.format(pair[0], pair[1])
                    full_copy_dict[st1].append(match)
                    full_copy_dict[st2].append(match)

                elif e_similarity_index[edge] >= 0.50 :
                    src, tgt =  edge
                    st1 = v_name[src]
                    st2 = v_name[tgt]
                    pair = e_file_pair[edge]
                    match = 'File {0} matches {1}\n'.format(pair[0], pair[1])
                    possible_copy_dict[st1].append(match)
                    possible_copy_dict[st2].append(match)
                else : pass

        # save a log file.
        with open(self.log_path+"/matching_files.txt", "w") as f :
            f.write("Following stundents have copied.\n\n")
            for i in full_copy_dict :
                f.write(unicode(i)+":\n\n")
                for line in full_copy_dict[i] :
                    f.write("  "+unicode(line)+'\n')

            f.write("\n\nFollowing students may have copied. Verify manually\n")
            for i in possible_copy_dict :
                f.write(unicode(i)+":\n\n")
                for line in possible_copy_dict[i] :
                    f.write("  "+unicode(line)+'\n')

        return full_copy_dict, possible_copy_dict

