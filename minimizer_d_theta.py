# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:56:00 2022

@author: Ernesto
"""


""" 
This is the implementation of Algo 3 of Kamiyamas paper.
Here we find a minimizer of d_theta following a more refined approach

"""
from time_expanded_network import time_expanded
import networkx as nx
import copy
from generate_instances import problem
#from algorithm_1_brute_force import argmin
from compute_d_theta_S import d_theta_S
import numpy as np
from matplotlib import pyplot as plt

#### testing: looks good with a instance of 2x2
def D_theta_epsilon(N, theta, epsilon):
    #Pre: N Nx.Digraph, time expanded network, theta integer, epsilon maximum static flow  dict in D_theta 
    #Post: Directed Graph D_theta_epsilon as defined in the japanese paper:
        # 1) For each arc l in the time expanded network,  we define a backwards arc l^(-1)
        # 2) The arc set in the D_theta_epsilon is the union of:
            # + A_1 = Arcs l in A_theta s.t. epsilon(l) < c_theta(l) (capacity in time expanded network)
            # + A_2 = Arcs l^(-1) s.t. epsilon(l) > 0
    M = copy.deepcopy(N)
    M.G.remove_edges_from(N.G.edges())
    
    
    for arc in list(N.G.edges()):
        if epsilon[str(arc[0])][str(arc[1])] < N.G.edges[arc[0], arc[1]]['capacity']:
            #print("edge added")
            M.G.add_edge(arc[0], arc[1])
        if epsilon[str(arc[0])][str(arc[1])] > 0:
            #print("edge added")
            M.G.add_edge(arc[1], arc[0])
    
    
    
    return M.G
        
            
            




def algo3(N, theta):
    #Pre: N instance of the problem
    #Post: Finds minimal subset of Vertices that minimizes d_theta. Outputted as set
    
    # Step 1: Find maximum static flow espilon in the time expanded Network D_theta
    
    D_theta = time_expanded(N, theta)
    flow_value, flow_dict = nx.maximum_flow(D_theta.G, "s_star", "s_moon")
    
    
    
    # Step 2: define Z_theta as the set of vertices V_theta (vertices in time expanded network) reachable from s_star in D_theta(epsilon) (use the has_path Networkx method)
    D_te = D_theta_epsilon(D_theta, theta, flow_dict)
    Z_theta = []
    X_theta = []
    
    
    for node in list(D_te.nodes()):
        if nx.has_path(D_te, "s_star", node):
            Z_theta.append(node)
     
    #print(Z_theta)           
    
            
    for node in N.S_plus:
        if str(node) + "_" + str(0)  in Z_theta:
            X_theta.append(node)
            
    for node in N.S_minus:
        if str(node) + "_" + str(theta) in Z_theta:
            X_theta.append(node)

    
  
            
        
    
    # Step 4: Output X_theta and halt
    
    return X_theta
### testing

# =============================================================================
# N = problem(5, 0.2, 0.2, 30)
# 
# for i in range(30):
#     print(str(d_theta_S(N, i, argmin(N, i)[0])) + "____" + str( d_theta_S(N, i, algo3(N, i))))
# 
# =============================================================================

# =============================================================================
# x = np.linspace(0, 30, 60)
# algo = []
# argmi = []
# 
# for i in range(30):
#     algo.append(d_theta_S(N, i, algo3(N, i)))
#     argmi.append(d_theta_S(N, i, argmin(N, i)[0]))
#     
# plt.plot(x, algo)
# plt.plot(x, argmi)
# 
# =============================================================================
