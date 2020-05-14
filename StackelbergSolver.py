'''
Created April 2020

@author: DLDAVIS
'''
DRAW_GRAPH = False
PRINT_FLAG = False
FAIL_THRESHOLD = 0.5
UTIL_D_COVERED = 3
UTIL_D_UNCOVERED = -1
UTIL_A_COVERED = -2
UTIL_A_UNCOVERED = 1

# SSG SOLVER CLASS
class StackelbergSolver():
    """
    StackelbergSecurityGame (SSG) is a bayesian normal-form stackelberg security game and holds the
    following values:
    -- defender: defender
    -- attacker: attacker/adversary
    -- c_x[l]: defender's payoffs (aka coverage vector)    
    -- Three  defense strategies are applied: non-deception, deception
    """
    def __init__(self, G, defender, attacker):
        self.G = G
        self.defender = defender
        self.attacker = attacker

        self.num_runs = 0
        self.attack_history = []
        self.comp_nodes = []
        self.a_t = None
        self.d_t = None
        
        #print("Defense budget = " + str(self.defender.budget) + ", Deg of GW network_node = " + str(self.attack_graph.getRandomGraph().num_neighbors(self.attack_graph.getRandomGraph().getGWNode())))

    def getCompromisedNodeCount(self): return len(self.comp_nodes)
    def getUncertainty(self): return self.attacker.getUncertainty()
    
    def initialize_game(self, num_nodes):
        # build and display initial graph
        self.G.reset()
        if DRAW_GRAPH: self.G.draw_graph()

    def play_repeated_games(self, num_nodes):
        self.num_runs += 1
        num_successful_attacks = 0
        num_attacks = 0
        num_uncertain_moves = 0
        
        self.initialize_game(num_nodes)
        
        game_count = 0
        res = True
        while res:
            res, successful_attack_count, attack_count, uncertain_move_count = self.play_static_game(game_count)
            if PRINT_FLAG: print("Completed a static SSG (" + str(uncertain_move_count) + ").")
            game_count += 1
            num_successful_attacks += successful_attack_count
            num_attacks += attack_count
            num_uncertain_moves += uncertain_move_count

            if DRAW_GRAPH: self.G.draw_graph()

        return game_count, num_successful_attacks, num_attacks, num_uncertain_moves 

    def play_static_game(self, game_count):
        u_d = None
        u_a = None

        self.d_t = self.defender.select_strategy(self.G, u_a, self.a_t)
        self.a_t = self.attacker.select_strategy(self.G, u_d, False, self.d_t)

        u_d, u_a, successful_att_count, att_count = self.compute_payoffs()
        
        res = self.get_system_condition()
        
        return res, successful_att_count, att_count, self.attacker.uncertain_move_count
    
    def compute_payoffs(self):
        u_d = 0
        u_a = 0
        
        attack_count = 0
        successful_attack_count = 0
        if self.a_t is not None and len(self.a_t) > 0:
            for attack_node_idx in range(len(self.a_t)):
                attack_node_id = self.a_t[attack_node_idx]
                if attack_count >= self.attacker.budget: break
                elif self.G.node_list[attack_node_id].is_quarantined(): break
                elif self.G.node_list[attack_node_id].is_compromised(): continue
                else:
                    attack_count += 1
                    
                    # check for removed or hidden edges
                    if attack_node_idx >= 1:
                        if self.G.is_decoy_edge(attack_node_id, self.a_t[attack_node_idx-1]):
                            if PRINT_FLAG: print("...DECOY EDGE!... [" + str(attack_node_id) + "]")
                            u_d += UTIL_D_COVERED
                            u_a += UTIL_A_COVERED
                            self.attacker.uncertain_move_count += 1
                            continue
                    
                    if self.d_t[attack_node_id] == 1:
                        if PRINT_FLAG: print("...BLOCKED ATTACK!... [" + str(attack_node_id) + "]")
                        u_d += UTIL_D_COVERED
                        u_a += UTIL_A_COVERED
                        #self.blocked_attacks.append(attack_node)
                        
                    else:
                        if PRINT_FLAG: print("...UNCOVERED ATTACK!... [" + str(attack_node_id) + "]")
                        successful_attack_count += 1
                        self.G.node_list[attack_node_id].set_to_compromised()
                        u_d += UTIL_D_UNCOVERED
                        u_a += UTIL_A_UNCOVERED

        return u_d, u_a, successful_attack_count, attack_count

    def get_system_condition(self):
        if self.G.node_list[self.G.goal_node_index].is_active() is False: 
            if PRINT_FLAG: print('System condition [' + str('False - Goal node compromised'))
            return False

        num_quarantined = 0
        num_compromised = 0
        for node in self.G.get_node_list():
            if node.is_quarantined(): num_quarantined += 1
            elif node.is_compromised(): num_compromised += 1
    
        if (num_compromised + num_quarantined) / len(self.G.get_node_list()) > FAIL_THRESHOLD:
            if PRINT_FLAG: print('System condition [' + str('False - Byzantine Failure') + ']: num_compromised = ' + str(num_compromised) + ', num_quarantined = ' + str(num_quarantined))
            return False
        
        if PRINT_FLAG: print('System condition [' + str('True') + ']: num_compromised = ' + str(num_compromised) + ', num_quarantined = ' + str(num_quarantined))
        return True
