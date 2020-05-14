'''
Modified on Dec 1, 2019

@author: DLDAVIS
'''

#import csv
from StackelbergSolver import StackelbergSolver
import numpy as np
import matplotlib.pyplot as plt
from defender import defender
from attacker import attacker
from rndGeometricGraph import network_environment

NUM_RUNS = 100
NUM_NODES = 100
DEFENSE_BUDGET = NUM_NODES / 2
ATTACK_BUDGET = 1
BAD_GUY_LOCATION_x = 25
BAD_GUY_LOCATION_y = 25
BAD_GUY_CONNECT_RANGE = 18
GOAL_NODE_INDEX = 94
DEFAULT_CONNECTION_RANGE = 18
PRINT_FLAG = False

def play():
    
    game_count_2d = None
    num_successful_attacks_2d = None
    num_attacks_2d = None
    num_uncertain_moves_2d = None
    hidden_edges_2d = None
    decoy_edges_2d = None
    
    for def_scheme in range(1,5):
        G = network_environment(False, NUM_NODES, DEFAULT_CONNECTION_RANGE, GOAL_NODE_INDEX)
        player_d = defender(DEFENSE_BUDGET, def_scheme)
        player_a = attacker(BAD_GUY_LOCATION_x, BAD_GUY_LOCATION_y, BAD_GUY_CONNECT_RANGE, ATTACK_BUDGET)
    
        solver = StackelbergSolver(G, player_d, player_a)
    
        game_count = np.zeros(NUM_RUNS, dtype=int)
        num_successful_attacks = np.zeros(NUM_RUNS, dtype=int)
        num_attacks = np.zeros(NUM_RUNS, dtype=int)
        num_uncertain_moves = np.zeros(NUM_RUNS, dtype=int)
        hidden_edges = np.zeros(NUM_RUNS, dtype=int)
        decoy_edges = np.zeros(NUM_RUNS, dtype=int)
        
        for idx in range(NUM_RUNS):
            [ game_count_val, num_successful_attacks_val, num_attacks_val, num_uncertain_moves_val ] = solver.play_repeated_games(NUM_NODES)
            game_count[idx] = game_count_val
            num_successful_attacks[idx] = num_successful_attacks_val
            num_attacks[idx] = num_attacks_val
            num_uncertain_moves[idx] = num_uncertain_moves_val
            hidden_edges[idx] = G.get_num_hidden_edges()
            decoy_edges[idx] = G.get_num_decoy_edges()
            
            player_d.clear_lists()
            player_a.clear_lists()
            
            if PRINT_FLAG: print('Game count = ' + str(game_count[idx]) + ', Num succ attacks = ' + str(num_successful_attacks[idx]) + ', Num attacks = ' + str(num_attacks[idx]) + ', Num uncertainty = ' + str(num_uncertain_moves[idx]))

        if game_count_2d is None: game_count_2d = game_count
        else: game_count_2d = np.vstack((game_count_2d, game_count))
        
        if num_successful_attacks_2d is None: num_successful_attacks_2d = num_successful_attacks
        else: num_successful_attacks_2d = np.vstack((num_successful_attacks_2d, num_successful_attacks))
        
        if num_attacks_2d is None: num_attacks_2d = num_attacks
        else: num_attacks_2d = np.vstack((num_attacks_2d, num_attacks))
        
        if num_uncertain_moves_2d is None: num_uncertain_moves_2d = num_uncertain_moves
        else: num_uncertain_moves_2d = np.vstack((num_uncertain_moves_2d, num_uncertain_moves))
        
        if hidden_edges_2d is None: hidden_edges_2d = hidden_edges
        else: hidden_edges_2d = np.vstack((hidden_edges_2d, hidden_edges))
        
        if decoy_edges_2d is None: decoy_edges_2d = decoy_edges
        else: decoy_edges_2d = np.vstack((decoy_edges_2d, decoy_edges))
        
    plot_results(game_count_2d, num_successful_attacks_2d, num_attacks_2d, num_uncertain_moves_2d)
        
    print ("---> Equilibrium achieved. DONE.")
    
    print("ATTACK SUCCESS PROBABILITY = " + str(np.sum(num_successful_attacks_2d[0]) / np.sum(num_attacks_2d[0])) + ', ' + str(np.sum(num_successful_attacks_2d[1]) / np.sum(num_attacks_2d[1])) + ', ' + str(np.sum(num_successful_attacks_2d[2]) / np.sum(num_attacks_2d[2])) + ', ' + str(np.sum(num_successful_attacks_2d[3]) / np.sum(num_attacks_2d[3])))
    print("AVG # of ATTACKS = " + str(np.sum(num_attacks_2d[0])/NUM_RUNS) + ', ' + str(np.sum(num_attacks_2d[1])/NUM_RUNS) + ', ' + str(np.sum(num_attacks_2d[2])/NUM_RUNS) + ', ' + str(np.sum(num_attacks_2d[3])/NUM_RUNS))
    print("AVG UNCERTAINTY = " + str(np.sum(num_uncertain_moves_2d[0])/NUM_RUNS) + ', ' + str(np.sum(num_uncertain_moves_2d[1])/NUM_RUNS) + ', ' + str(np.sum(num_uncertain_moves_2d[2])/NUM_RUNS) + ', ' + str(np.sum(num_uncertain_moves_2d[3])/NUM_RUNS))
    print("AVG MTTSF = " + str(np.sum(game_count_2d[0])/NUM_RUNS) + ', ' + str(np.sum(game_count_2d[1])/NUM_RUNS) + ', ' + str(np.sum(game_count_2d[2])/NUM_RUNS) + ', ' + str(np.sum(game_count_2d[3])/NUM_RUNS))
    print("# of HIDDEN EDGES = " + str(np.sum(hidden_edges_2d[0])/NUM_RUNS) + ', ' + str(np.sum(hidden_edges_2d[1])/NUM_RUNS) + ', ' + str(np.sum(hidden_edges_2d[2])/NUM_RUNS) + ', ' + str(np.sum(hidden_edges_2d[3])/NUM_RUNS))
    print("# of DECOY EDGES = " + str(np.sum(decoy_edges_2d[0])/NUM_RUNS) + ', ' + str(np.sum(decoy_edges_2d[1])/NUM_RUNS) + ', ' + str(np.sum(decoy_edges_2d[2])/NUM_RUNS) + ', ' + str(np.sum(decoy_edges_2d[3])/NUM_RUNS))
    
def plot_results(game_count, num_successful_attacks, num_attacks, num_uncertain_moves):
    asp2D = []
    for row in range(4):
        asp1D = []
        for col in range(NUM_RUNS):
            val = num_successful_attacks[row][col] / num_attacks[row][col]
            asp1D.append(val)
        asp2D.append(asp1D)
        
    x1 = np.arange(1,NUM_RUNS+1)
    
    _, (ax1, ax2, ax3) = plt.subplots(1,3, sharex=True)
    
    ax1.plot(x1, game_count[0], label='IDS only')
    ax1.plot(x1, game_count[1], label='IDS + EC')
    ax1.plot(x1, game_count[2], label='IDS + ED')
    ax1.plot(x1, game_count[3], label='IDS + EC + ED')
    ax1.set_title('Mean Time to Security Failure')
    ax1.legend()

    ax2.plot(x1, asp2D[0], label='IDS only')
    ax2.plot(x1, asp2D[1], label='IDS + EC')
    ax2.plot(x1, asp2D[2], label='IDS + ED')
    ax2.plot(x1, asp2D[3], label='IDS + EC + ED')
    ax2.set_title('Attack Success Probability')
    ax2.set_ylim(0,1.1)
    ax2.legend()
    
    ax3.plot(x1, num_uncertain_moves[0], label='IDS only')
    ax3.plot(x1, num_uncertain_moves[1], label='IDS + EC')
    ax3.plot(x1, num_uncertain_moves[2], label='IDS + ED')
    ax3.plot(x1, num_uncertain_moves[3], label='IDS + EC + ED')
    ax3.set_title('Attacker Uncertainty')
    ax3.legend()
    plt.show()

    if PRINT_FLAG: print('Plots completed.')

if __name__ == '__main__':
    play()
