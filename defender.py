'''
Created on May 2020

@author: DLDAVIS
'''

import numpy as np
from numpy import random
import math

IDS_ONLY = 1
IDS_EC = 2
IDS_ED = 3
IDS_EC_ED = 4
PRINT_FLAG = False

class defender:
    def __init__(self, def_budget, scheme):
        self.budget = def_budget
        self.blocked_nodes = []
        self.decoy_edges = []
        self.scheme = scheme

    def select_strategy(self, G, inputs, a_t):
        num_ids = num_ec = num_ed = 0
        G.unhide_edges_and_remove_decoys()
        
        # select strategy by scheme
        if self.scheme == IDS_ONLY:
            num_ids = self.budget
        elif self.scheme == IDS_EC:
            num_ids = round(self.budget * 0.9)
            num_ec = round(self.budget * 0.2)
        elif self.scheme == IDS_ED:
            num_ids = round(self.budget * 0.9)
            num_ed = round(self.budget * 0.2)
        elif self.scheme == IDS_EC_ED:
            num_ids = round(self.budget * 0.9)
            num_ec = round(self.budget * 0.1)
            num_ed = round(self.budget * 0.1)
        
        ids = self.generate_stochastic_ids_vector(len(G.node_list), num_ids)

        self.select_edges_to_hide(G, num_ec, a_t)
        
        self.select_decoy_edges(G, num_ed, a_t)
        
        return ids
    
    def clear_lists(self):
        self.blocked_nodes = []
        self.hidden_edges = []
        self.decoy_edges = []
  
    def takeSecond(self, elem):
        return elem[1]

    def generate_stochastic_ids_vector(self, num_nodes, budget):
        tmp = []
        for idx in np.arange(0,num_nodes):
            tmp.append([idx, random.rand()])
            
        tmp.sort(key=self.takeSecond)  
        
        sorted_vector = []
        for idx in np.arange(0,round(budget)): 
            sorted_vector.append(tmp[idx][0])
        
        ids_vector = np.zeros(num_nodes, dtype=int)
        for idx in sorted_vector: ids_vector[idx] = 1

        return ids_vector

    def select_edges_to_hide(self, G, budget, a_t):
        tmp_budget = budget
        if a_t is not None and len(a_t) > 0:
            for idx in np.arange(len(a_t)-1, 0, -1):
                if tmp_budget > 0:
                    # move on if hidden neighbors are present
                    if len(G.get_hidden_neighbors(a_t[idx])) > 0: continue
                    #if len(G.get_decoy_neighbors(a_t[idx])) > 0: continue
    
                    if PRINT_FLAG: print("...Hiding edge (" + str(tmp_budget) + ") #" + str(idx))
                    self.add_hidden_edges(G, idx)
                    tmp_budget -= 1
                else: break
        
        cnt = 0
        while tmp_budget > 0:
            rnd_idx = random.randint(len(G.node_list)-1)
            if len(G.get_hidden_neighbors(rnd_idx)) > 0 and cnt < 10:
                cnt += 1
                continue
            
            if PRINT_FLAG: print("...hiding edge (" + str(tmp_budget) + ") #" + str(rnd_idx))
            self.add_hidden_edges(G, rnd_idx)
            tmp_budget -= 1
            if tmp_budget <= 0: break;
                        
    def add_hidden_edges(self, G, idx):
        # pick up to half of the current edges to hide for the selected node
        neighbors = []
        for index2 in range(len(G.adj_matrix[idx])):
            if G.adj_matrix[idx][index2] == 1: neighbors.append(index2)
        
        num_hidden_edges = math.floor(len(neighbors)/2) # number of edges to hide
        for index2 in range(idx+1, len(G.node_list)):
            if num_hidden_edges <= 0: break
            
            if G.adj_matrix[idx][index2] == 1:
                G.adj_matrix[idx][index2] = -1
                G.adj_matrix[index2][idx] = -1
                num_hidden_edges -= 1
                
    
    def select_decoy_edges(self, G, budget, a_t):
        tmp_budget = budget
        if a_t is not None and len(a_t) > 0:
            for idx in np.arange(len(a_t)-1, 0, -1):
                if tmp_budget > 0:
                    # move on if decoy neighbors are present
                    if len(G.get_decoy_neighbors(a_t[idx])) > 0: continue
    
                    self.add_decoy_edges(G, idx)
                    tmp_budget -= 2
                else: break

        
        cnt = 0
        while tmp_budget > 0:
            rnd_idx = random.randint(len(G.node_list)-1)
            if len(G.get_decoy_neighbors(rnd_idx)) > 0 and cnt < 10:
                cnt += 1
                continue
            
            self.add_decoy_edges(G, rnd_idx)
            tmp_budget -= 2
                        
    def add_decoy_edges(self, G, idx):
        neighbors = []
        for index2 in range(len(G.adj_matrix[idx])):
            if G.adj_matrix[idx][index2] == 1: neighbors.append(index2)
        
        num_decoy_edges = math.floor(len(neighbors)/2) # number of edges to hide
        for index2 in range(idx+1, len(G.node_list)):
            if num_decoy_edges <= 0: break

            if G.adj_matrix[idx][index2] == 0:
                G.adj_matrix[idx][index2] = 2
                G.adj_matrix[index2][idx] = 2
                num_decoy_edges -= 1
