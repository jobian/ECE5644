'''
Created on May 2020

@author: DLDAVIS
'''
from math import sqrt

class attacker:
    def __init__(self, x, y, conn_range, budget=1):
        self.budget = budget
        self.current_ags = []
        self.available_ags = []
        self.attack_location = [x, y]
        self.attacker_range = conn_range
        self.uncertain_move_count = 0
        
    def clear_lists(self):
        self.current_ags = []
        self.available_ags = []

    # Strategy type: 'True' 
    def select_strategy(self, G, inputs, is_pure_strategy, d_t):
        # check for inactive nodes -- remove any AGs with inactive nodes
        self.refresh_inactive_nodes_list(G)
        
        # generate all available attack graphs (best AG per neighbor node)
        self.generate_ags(G)

        return self.get_best_next_ag(G)

    def get_best_next_ag(self, G):
        ag_high = None
        u_high = 0
        u_val = 0
        
        for ag in self.available_ags:
            u_val = self.score_ag(G, ag)
            if u_val > u_high:
                u_high = u_val
                ag_high = ag
                
        # remove selected AG from the 'available' list and add to the 'current' list
        if ag_high is not None:
            self.available_ags.remove(ag_high)
            self.current_ags.append(ag_high)

        return ag_high
    
    def score_ag(self, G, ag):
        if ag is None or len(ag) == 0: return -1
        ag_last_node = G.node_list[ag[-1]].get_xy_coordinate()
        goal = G.node_list[G.goal_node_index].get_xy_coordinate()
        delta = round(sqrt( pow((ag_last_node[0] - goal[0]), 2) + pow((ag_last_node[1] - goal[1]), 2) ), 4)

        if delta == 0: return 100
        return 1 / (delta + (len(ag) - 1))
    
    # refresh current_ags list    
    def generate_ags(self, G):
        # get nodes within connection of the attacker
        if len(self.current_ags) == 0 and len(G.get_inactive_node_ids()) == 0 and (self.available_ags is None or len(self.available_ags) == 0):
            for node in G.get_node_list():
                if node.is_within_range(self.attack_location, self.attacker_range) and node.get_node_id() >= 5:
                    if self.available_ags is None: self.available_ags = []
                    if node.get_node_id not in self.available_ags: self.available_ags.append([node.get_node_id()])
        
        # identify and select up to 2 ACTIVE, neighbor nodes (highest utilities) to extend the AG list
        for ag in self.current_ags:
            top_neighbors_idx = [-1, -1]
            top_neighbors_score = [0, 0]
            
            if len(ag) == 0: continue
            last_node_idx = ag[-1]
            
            node_neighbors = G.get_neighbors(last_node_idx)
            
            # Add in the fake/decoy neighbors
            fake_neighbors = G.get_decoy_neighbors(last_node_idx)
            for fake_neighbor in fake_neighbors: node_neighbors.append(fake_neighbor)
            
            for neighbor in node_neighbors:
                neighbor_id = neighbor.get_node_id()
                
                # Ignore (and increment) hidden edges
                if G.is_hidden_edge(last_node_idx, neighbor_id):
                    self.uncertain_move_count += 1
                    continue
                
                if neighbor_id in ag or neighbor_id in G.get_inactive_node_ids(): 
                    continue
                
                tmp_ag = ag.copy()
                tmp_ag.append(neighbor_id)
                if tmp_ag in self.current_ags or tmp_ag in self.available_ags: continue
                tmp_ag_score = self.score_ag(G, tmp_ag)
                
                if top_neighbors_score[1] >= top_neighbors_score[0]:
                    if tmp_ag_score > top_neighbors_score[0]:
                        top_neighbors_idx[0] = neighbor_id
                        top_neighbors_score[0] = tmp_ag_score
                elif top_neighbors_score[0] > top_neighbors_score[1]:
                    if tmp_ag_score > top_neighbors_score[1]:
                        top_neighbors_idx[1] = neighbor_id
                        top_neighbors_score[1] = tmp_ag_score
                        
            # append top two neighbors
            if top_neighbors_score[0] > 0:
                tmp_ag = ag.copy()
                tmp_ag.append(top_neighbors_idx[0])
                self.available_ags.append(tmp_ag)
            
            if top_neighbors_score[1] > 0:
                tmp_ag = ag.copy()
                tmp_ag.append(top_neighbors_idx[1])
                self.available_ags.append(tmp_ag)
            
        return
        
    def refresh_inactive_nodes_list(self, G):
        # iterate through current_ags list and check for inactive nodes (remove them)
        for ag in self.current_ags:
            for node_id in ag:
                if G.node_list[node_id].is_quarantined():
                    self.current_ags.remove(ag)
                    break
        
        # iterate through available_ags list and check for inactive nodes (remove them)
        for ag in self.available_ags:
            for node_id in ag:
                if G.node_list[node_id].is_quarantined():
                    self.available_ags.remove(ag)
                    break
