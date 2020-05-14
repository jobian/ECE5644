'''
Modified on Dec 1, 2019

@author: DLDAVIS
'''

from math import sqrt

class network_node():
    def __init__(self, node_id, xy_coordinate, num_neighbors, default_connect_range=100, is_gateway=False):
        super(network_node, self).__init__()
        
        self.node_id = node_id # doubles as node index
        self.p_pos = xy_coordinate
        self.num_neighbors = num_neighbors
        self.status = 'A' # A: Active, C: compromised, Q: quarantined
        self.is_target = False
        self.connection_range = default_connect_range

    def set_to_active(self): self.status = 'A'
    def is_active(self): return self.status == 'A'
    def is_compromised(self): return self.status == 'C'
    def set_to_compromised(self): self.status = 'C'
    def is_quarantined(self): return self.status == 'Q'
    def set_to_quarantined(self): self.status = 'Q'
    def is_target_flag(self): return self.is_target
    def set_target_flag(self, flag): self.is_target = flag

    def is_gw_node(self): return self.is_gateway
    def get_node_id(self): return self.node_id

    def get_xy_coordinate(self): return self.p_pos
    def set_xy_coordinate(self, x, y): self.p_pos = [x, y]
    
    def get_connection_range(self): return self.connection_range
    def set_connection_range(self, conn_range): self.connection_range = conn_range

    #def get_num_neighbors(self): return self.num_neighbors
    #def set_num_neighbors(self, num_neighbors): self.num_neighbors = num_neighbors

    def compute_euclidean_distance(self, node):
        x1 = self.get_xy_coordinate()[0]
        y1 = self.get_xy_coordinate()[1]
        x2 = node.get_xy_coordinate()[0]
        y2 = node.get_xy_coordinate()[1]
        #print ("get_euclidean_distance (x1,y1) = (" + str(x1) + ", " +  str(y1) + "), (x2,y2) = (" + str(x2) + ", " +  str(y2) + ")")
        #print ("get_euclidean_distance: node1 = " + str(node1) + ", node2 = " +  str(node2) + ", dist = " + str(round(sqrt( pow((x2 - x1), 2) + pow((y2 - y1), 2) ), 4)))
    
        dist = round(sqrt( pow((x2 - x1), 2) + pow((y2 - y1), 2) ), 4)
        return dist #< DEFAULT_CONNECTIVITY_RANGE

    def is_within_range(self, node_loc, conn_range=-1):
        x1 = self.get_xy_coordinate()[0]
        y1 = self.get_xy_coordinate()[1]
        x2 = node_loc[0]
        y2 = node_loc[1]
        if conn_range < 0: conn_range = self.connection_range
        #print ("get_euclidean_distance (x1,y1) = (" + str(x1) + ", " +  str(y1) + "), (x2,y2) = (" + str(x2) + ", " +  str(y2) + ")")
        #print ("get_euclidean_distance: node1 = " + str(node1) + ", node2 = " +  str(node2) + ", dist = " + str(round(sqrt( pow((x2 - x1), 2) + pow((y2 - y1), 2) ), 4)))
    
        return round(sqrt( pow((x2 - x1), 2) + pow((y2 - y1), 2) ), 4) < conn_range
    