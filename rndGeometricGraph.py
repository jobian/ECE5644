'''
Modified on Dec 1, 2019

@author: DLDAVIS
'''
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from network_node import network_node

PRINT_FLAG = False
ONE_SEC_DELAY = False

class network_environment:
    def __init__(self, isDynamic, num_nodes, default_connect_range, goal_node_index):
        self.is_dynamic_network = isDynamic
        self.NUM_NODES = num_nodes
        self.G = []
        self.goal_node_index = goal_node_index
        self.node_list = [] # list of network_node objects
        self.hidden_edges = []
        self.adj_matrix = None
        self.base_stations = []
        self.reset_network(default_connect_range)
                
    def copy_network_env(self): return self
    def isDynamic(self): return self.is_dynamic_network
    def isConnected(self): return nx.is_connected(self.G)
    def getGraph(self): return self.G;
    def get_adj_matrix(self):
        if self.adj_matrix is None: raise NotImplementedError
        return self.adj_matrix
    def get_node_list(self): return self.node_list
    def update_node(self, node, idx): self.node_list[idx] = node
    def reset_network(self, default_connect_range):
        self.buildGraph(default_connect_range)

    '''
    def hide_edge(self, node1_idx, node2_idx):
        if self.adj_matrix[node1_idx][node2_idx] == 1:
            self.adj_matrix[node1_idx][node2_idx] = 2
        
    def get_hidden_edges(self):
        if self.adj_matrix is None: raise NotImplementedError

        hidden_edges = []
        for i in range(len(self.adj_matrix)):
            for j in range (i+1, len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] == 2: hidden_edges.append(str(i) + "," + str(j))
                
        return hidden_edges
    '''
    def get_comp_nodes(self):
        comp_nodes = []
        for node in self.node_list:
            if node.is_compromised_flag() == True:
                comp_nodes.append(node)
                
        return comp_nodes
    
    def get_inactive_node_ids(self):
        in_nodes = []
        for node in self.node_list:
            if node.is_active() == False:
                in_nodes.append(node.get_node_id())
                
        return in_nodes
    
    def buildGraph(self, default_connect_range):
        orig_node_locations = [(99, 94), (34, 71), (62, 17), (33, 44), (63, 16), (11, 154), (7, 182), (82, 140), (57, 14), (24, 20), (4, 27), (180, 156), (83, 198), (62, 197), (4, 185), (42, 127), (55, 117), (89, 136), (80, 156), (45, 137), (197.71187416708744, 6.09858928540612), (195.36662458248065, 94.80704372310669), (44.619103227750934, 195.5202435723903), (66.59983143896014, 166.20721846743334), (191.4940811204589, 44.38019239128821), (114.36756345009755, 190.46391269423663), (172.01879743907978, 72.18996030350166), (118.36782673413462, 60.03613118484841), (176.66488446583153, 179.15843231833182), (14.085556578054253, 108.59132565724305), (65.81838384849273, 81.40318142842595), (12.517734631328947, 118.8483501444943), (140.82672220728978, 14.64522537888091), (61.19661595227386, 76.03892689655576), (124.0258869111258, 109.11019300373049), (163.22200369778403, 23.08535698084595), (54.199204306771605, 169.10017623087973), (34.96839553901052, 39.13009078502867), (159.44715565053917, 96.5822602513014), (121.11267381529491, 133.86379440901578), (158.06887995790552, 124.35336731642505), (121.55263758216182, 166.5157675824778), (99.01838560334062, 118.48962890507866), (196.30233102214223, 102.60955626602808), (54.0810930416328, 52.59642872363117), (174.55001372223418, 44.20599442585964), (133.00673275335123, 185.3274366885677), (29.782156014855545, 54.737108181945906), (148.96371521931954, 194.70040431255825), (155.92694881205765, 66.9692281548237), (167.8372635809594, 38.74671505501554), (9.552612032279484, 76.03996436739932), (195.12151049201512, 16.315892946696774), (86.01925178821557, 172.3705782438163), (46.52882507701073, 82.86172416447282), (159.8467076624574, 91.94867167827101), (120.98985503305137, 36.414586206384755), (174.29033731028494, 69.1616076952309), (60.96638282933191, 42.268116347282), (2.8077472262972414, 128.39682273887497), (134.8907946094975, 1.4891374912403776), (170.6766505159174, 53.19706145817227), (95.39623002028634, 0.7264286558636535), (97.86445052484913, 32.74261348676284), (108.5567620327883, 118.61699768367724), (122.88220503282498, 19.74878902618591), (138.64672820128544, 81.84285214023383), (183.44763078202192, 0.9619677699737705), (192.7803090802737, 198.27005111365176), (43.25178526996256, 147.73838436239794), (101.08605699977656, 90.14939830249045), (111.67271589179326, 106.9442798099639), (119.00702386474609, 47.42002772167482), (168.04685775711758, 115.36584428563515), (12.859493852695515, 40.73591178315405), (68.20958420927461, 0.3392173644863883), (129.10256890092074, 13.82246810824357), (46.74179582713649, 81.54943430270427), (23.61115664457103, 171.54054342681567), (184.41217619904714, 93.36273168099017), (67.43449181511502, 103.7506024230217), (93.02073215165458, 81.09278426662489), (100.59117569489659, 34.13516129814269), (171.67109261902772, 179.3636221597296), (149.01437614522035, 145.9556800375271), (147.32451758790987, 68.85817392254714), (180.67327090878365, 14.570535091410196), (190.99975121233828, 196.29559811806556), (74.46274778379328, 75.2363515869264), (101.10809560169581, 4.448172457230926), (112.7954318581432, 5.040306509308201), (169.72926654861203, 137.65687717248758), (170.99536970998133, 13.56272074649465), (22.317144642175336, 103.6428879256401), (199.69543362196183, 25.800376473560462), (166.82052305571372, 124.75592849870311), (150.15014012408898, 7.559976296412074), (105.932602759226, 80.05634840519468), (93.57247016227421, 103.3125117297583), (185.05846785927667, 113.92491482057426)]
        node_locations = []
        for idx in range(len(orig_node_locations)):
            node_locations.append([orig_node_locations[idx][0] / 2.0, orig_node_locations[idx][1] / 2.0])
            if PRINT_FLAG: print('Node locations: [' + str(idx) + ']: ' + str(node_locations[idx][0]) + ',' + str(node_locations[idx][1]))

        if self.NUM_NODES > len(node_locations): self.NUM_NODES = len(node_locations)
        elif self.NUM_NODES < len(node_locations): node_locations = node_locations[0 : self.NUM_NODES]
        #self.pos = {idx: (node_locations[idx][0], node_locations[idx][1]) for idx in range(len(node_locations))}
        self.pos = {idx: (node_locations[idx][0], node_locations[idx][1]) for idx in range(len(node_locations))}

        self.adj_matrix = np.zeros((len(node_locations), len(node_locations)))
        
        # Construct graph of nodes only (no edges)
        self.G = nx.random_geometric_graph(len(node_locations), 0, pos=self.pos)
        
        # Configure node sizes and colors
        self.color_map = []
        self.node_sizes = []
        self.node_list = []
        for idx in range(len(node_locations)):
            self.node_list.append(network_node(idx, node_locations[idx], 0, default_connect_range))
            if (idx == self.goal_node_index):
                self.color_map.append('orange') # color master gateway
                self.node_sizes.append(30)
                '''
                elif (idx < 5): 
                    self.color_map.append('orange') # color regional gateways
                    self.node_sizes.append(80)
                '''
            else:
                self.color_map.append('blue') # color regular nodes
                self.node_sizes.append(30)
        '''
        #print('Graph - count = ' + str(len(node_locations)) + ', color map size = ' + str(len(self.color_map)))
        '''
        # Create adjacency matrix
        self.update_adj_matrix()
        '''
        # Interconnect the gateway nodes
        # self.connect_gw_nodes()
        '''
        
        # Check to ensure that the graph is sufficiently connected
        if PRINT_FLAG: print('Is the graph connected? ' + str(self.isConnected()))

    def draw_graph(self):
        self.recolor_graph()
                    
        if PRINT_FLAG: print('Num nodes: ' + str(self.G.number_of_nodes()) + ', len node_list = ' + str(len(self.node_list)) + ', len node_sizes = ' + str(len(self.node_sizes)) + ', len color_map = ' + str(len(self.color_map)))
        plt.clf()
        nx.draw(self.G, self.pos, with_labels=False, node_size=self.node_sizes, node_color=self.color_map, width=0.25)
        plt.xlim(-1.05, 101.05)
        plt.ylim(-1.05, 101.05)
        plt.ion()
        if ONE_SEC_DELAY: plt.pause(1)
        plt.show()

    def recolor_graph(self):
        for idx in range(len(self.node_list)):
            if self.node_list[idx].is_compromised():
                self.color_map[idx] = 'yellow' # compromised
            elif self.node_list[idx].is_active():
                self.color_map[idx] = 'blue' # active + not compromised
            elif self.node_list[idx].is_quarantined():
                self.color_map[idx] = 'red' # not active (removed from the network)
    
    def reset(self):
        # set all nodes back to 'Active'
        for idx in range(len(self.node_list)): self.node_list[idx].set_to_active()
        self.unhide_edges_and_remove_decoys()
                        
    def update_adj_matrix(self):
        # Generate edges & build the adjacency matrix
        for x in range(len(self.node_list)):
            for y in range(x+1,len(self.node_list)):
                if True:
                    #if self.get_neighborhood(x) == self.get_neighborhood(y):
                        #print("DIST(" + str(x) + ', ' + str(y) + ") x1 = " + str(self.node_list[x].get_xy_coordinate()[0]) + ', y1 = ' + str(self.node_list[x].get_xy_coordinate()[1])  + " -- x2 = " + str(self.node_list[y].get_xy_coordinate()[0]) + ', y2 = ' + str(self.node_list[y].get_xy_coordinate()[1]))
                    dist = self.node_list[x].compute_euclidean_distance(self.node_list[y])
                    if dist <= self.node_list[x].connection_range and dist <= self.node_list[y].connection_range:
                        self.adj_matrix[x][y] = 1 # Update adjacency matrix
                        self.adj_matrix[y][x] = 1
                        self.G.add_edge(x,y) # Add edges to graph
    
    def get_neighbors(self, node_id):
        neighbors = []
        for idx in range(len(self.node_list)):
            if idx != node_id and self.adj_matrix[node_id][idx] == 1:
                neighbors.append(self.node_list[idx])

        return neighbors
    
    def get_decoy_neighbors(self, node_id):
        decoys = []
        for idx2 in range(len(self.adj_matrix[node_id])):
            if self.adj_matrix[node_id][idx2] == 2:
                decoys.append(self.node_list[idx2])
                
        return decoys
        
    def get_num_decoy_edges(self):
        cnt = 0
        for i in np.arange(0,len(self.node_list)):
            for j in np.arange(i+1,len(self.node_list)):
                if self.adj_matrix[i][j] == 2:
                    cnt += 1
                
        return cnt
        
    def get_hidden_neighbors(self, node_id):
        ghosts = []
        for idx2 in range(len(self.adj_matrix[node_id])):
            if self.adj_matrix[node_id][idx2] == -1:
                ghosts.append(self.node_list[idx2])
                
        return ghosts
        
    def get_num_hidden_edges(self):
        cnt = 0
        for i in np.arange(0,len(self.node_list)):
            for j in np.arange(i+1,len(self.node_list)):
                if self.adj_matrix[i][j] == -1:
                    cnt += 1
                
        return cnt
        
    def unhide_edges_and_remove_decoys(self):
        for i in np.arange(0,len(self.node_list)):
            for j in np.arange(0,len(self.node_list)):
                if self.adj_matrix[i][j] == -1:
                    self.adj_matrix[i][j] = 1
                
        for i in np.arange(0,len(self.node_list)):
            for j in np.arange(0,len(self.node_list)):
                if self.adj_matrix[i][j] == 2:
                    self.adj_matrix[i][j] = 0
    
    def is_hidden_edge(self, node1, node2):
        if self.adj_matrix[node1][node2] == -1:
            return True
        return False
        
    def is_decoy_edge(self, node1, node2):
        if self.adj_matrix[node1][node2] == 2:
            return True
        return False