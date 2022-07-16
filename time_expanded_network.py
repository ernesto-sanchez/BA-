# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:03:43 2022

@author: Ernesto Sanchez



The main function of this script returns the time expanded network as defined in Kamiyama.
We use it to find a minimizer for d_theta following algo 3 of his paper. 

PRE: - Nonnegative integer Theta
     - Instance of problem
     
     
    
    
POST: A new ontance of the problem with a new graph s.t:
    
    
    - Vertex set = Old vertex set U supersource s_star and a vertex v_t for every vertex v
        in V adn every time t in {0, 1, ..., theta}
        
      - Arc set is the union of 
              - The old arcs
              - A_theeta_1: Contains arc a_t from u_t to v_(t+t_time(a)) for each arc a = (u,v) in A and each integer t in {0, 1, ..., theta - t_time(a)}
              - A_theta_2: Contains arc h_t_v from v_t to v_(t+1) for each vertex v in V and each integer in {0, 1, ..., theta -1}
              - A_theta_3: Contains arc a_v from a s_star to v_0 for each v in V
              
              
      - Capacity function: - Old arcs get the same capacity
              - Arcs in A_theta_1 get the same capacity as the old arcs they are generated from 
              - Arcs in A_theta _2 have infinite capacity
              - Arcs in A_theta_3 have the demand of the original terminal as capacity
            
            

"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import math
from generate_instances import problem
import copy





def time_expanded(N, theta):
    #PRE :- Nonnegative integer Theta
    # - Instance of problem
    #POST: Time extended network as defined in Kamiyamas paper. Required as input for "minimizer_d_theta"
    # it is outputted as an object of the class Problem. Returns only the graph
    
    
    
    old_edges = list(N.G.edges(data = True))
    old_nodes = list(N.G.nodes)
    terminals = N.S_plus + N.S_minus 
    S_plus = N.S_plus
    S_minus = N.S_minus
    
    
    
    M = copy.deepcopy(N)
    
    #First rename the original nodes with the appendix "_0" and then create the new ones
    
    mapping = {}
    for node in old_nodes:
        mapping[node] = str(node) + "_" + str(0)
        
    M.G = nx.relabel_nodes(M.G, mapping)
    
    for node in old_nodes:
        
        for i in range(1, theta +1):
            
            M.G.add_node("{}_{}".format(node, i))
    
    
    M.G.add_node("s_star") #supersource
    M.G.add_node("s_moon") #supersink
    
    O = copy.deepcopy(M)
    M.G.remove_edges_from(O.G.edges())
    
    ## Adding the arcs
    ## A_theta_1
    
    for edge in old_edges:
        for t in range(theta - int(edge[2]["t_time"]) + 1):
            
            M.G.add_edge(str(edge[0]) + "_" + str(t), str(edge[1]) + "_" + str(t + int(edge[2]["t_time"])), capacity = edge[2]["capacity"] )
        
    ## A_theta_2
    
    for node in old_nodes:
        
        
        
        for t in range(theta):
            
            M.G.add_edge(str(node) + "_" + str(t), str(node) + "_" + str(t+1), capacity = float('inf'))
            
    ## A_theta_3
        
    for node in S_plus:
    
        M.G.add_edge('s_star', str(node) + "_" + str(0), capacity = M.b[node] )
        
    for node in S_minus:
      
        M.G.add_edge(str(node) + "_" + str(theta),'s_moon' , capacity = -M.b[node] )
          
    
    return M









##### TESTING
# =============================================================================
# 
# N = problem(4, 0.15, 0.15, 40)
# M = time_expanded(N, 3)
# 
# pos = nx.spring_layout(M.G, dim = 3, seed = 779)
#  
# 
# plt.figure(dpi = 1200)
# =============================================================================
# =============================================================================
# 
# nx.draw_networkx(M.G ,pos, with_labels=True,font_size = 6, arrows = True)
# nx.draw_networkx_nodes(M.G,pos,  nodelist= M.S_minus, node_color="tab:red")
# nx.draw_networkx_nodes(M.G, pos, nodelist= M.S_plus, node_color="tab:green")
# 
# 
# =============================================================================
