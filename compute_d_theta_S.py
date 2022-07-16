# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:10:10 2022

@author: Ernesto
"""



###The aim of this script ids to compute the fucntion d

import networkx as nx
import matplotlib.pyplot as plt
from generate_instances import problem
import random

import numpy as np


## Testing with a specific instance of teh problem with a very particular d_theta function
# =============================================================================
# 
# 
# N = problem(3, 0.5, 0.5, 30)
#     
# G = nx.DiGraph()
# G.add_edge("S_1", "a", capacity=1.0, t_time = 1)
# G.add_edge("S_2", "a", capacity=1.0, t_time = 6)
# G.add_edge("S_3", "a", capacity=1.0, t_time = 14)
# # G.add_edge("S_4", "a", capacity=1.0, t_time = 50)
# # G.add_edge("S_5", "a", capacity=1.0, t_time = 50)
# G.add_edge("a", "b", capacity =float("inf"),  t_time = 1)
# 
# S_minus = {"b"}
# S_plus = {"S_1", "S_2", "S_3"}
#     
# 
#     
# b = {
#      "S_1" : 1,
#      "S_2" : 1,
#      "S_3" : 1,
#      #"S_4" : 1,
#      #"S_5" : 1,
#      "b" : -5}    
# 
# N.G = G
# N.S_plus = list(S_plus)
# N.S_minus = list(S_minus)
# N.b = b
# =============================================================================
        

    


# =============================================================================
# 
# pos = nx.spring_layout(N.G, seed = 1288)
#  
# nx.draw_networkx(N.G,pos , with_labels=True,font_size = 6, arrows = True)
# nx.draw_networkx_nodes(N.G, pos, nodelist= N.S_plus, node_color="tab:red")
# nx.draw_networkx_nodes(N.G, pos, nodelist= N.S_minus, node_color="tab:green")
# 
# 
# 
# =============================================================================
    

#=============================================================================
# Test of the intence of problem   
# =============================================================================
# prb = problem(4, 0.15, 0.15, 100)
# H = prb.G
# b = prb.b
# 
# S_plus = prb.S_plus
# S_minus = prb.S_minus
# 
# b = prb.b
# 
# 
# #generate random S to test the function
#    S = random.sample(S_plus + S_minus, 2)
# 
# 
# 
# 
# #N_S = extended_network_1(H, S, S_plus, S_minus)
# 
#       
# pos = nx.spring_layout(H, seed = 1288)
# 
# nx.draw_networkx(H,pos , with_labels=True,font_size = 6, arrows = True)
# nx.draw_networkx_nodes(H, pos, nodelist= prb.S_plus, node_color="tab:red")
# nx.draw_networkx_nodes(H, pos, nodelist=prb.S_minus, node_color="tab:green")
# 
# 
# =============================================================================
#=============================================================================


def Ford_Fulkerson(N, theta):
    # PRE : Extended network with supersource and supersink "SOURCE" and "SINK", 
    # as outputted by extended_network_1, time horizon theta  
    
    #POST : compute feasible static s-t flow x maximixing $ T \cdot |x| 
    # - Sum {t_e \cdot x_e}
    # We do this by computing a static mincost circulation in the extended
    # network outputted by extended_network_2   Question : Ciculation = 
    # every node has demand 0?
    
    N_tilda = extended_network_2(N, theta)
    
    #print(N_tilda.edges.data())
    
    flowCost, flowDict =  nx.network_simplex(N_tilda, capacity = 'capacity', weight ='t_time')
# =============================================================================
#     print("cost of flow is" + str(flowCost))
#     print(flowDict)
#     print ("value of flow is: " + str(flowDict["SINK"]["SOURCE"]))
#     
# =============================================================================
    return flowCost
    

   
    
    
    


#### Problem : "SOURCE" gets joined to all the sources not the ones that are also in S

def extended_network_1(N, S):
    # Pre : N: instance of problem
    # Computes the extended network needed to compute o : 
    #     Add supersource s and supersink t with arcs of infinite
    #     capcity and 0 transit time connecting:
    #         s to S intersec. S_plus
    #         t to S_minus without S
    # Post : Network N with desired properties
    
    Graph = nx.DiGraph(N.G)
    
    for s in S:
        if s in N.S_plus:
            Graph.add_edge("SOURCE", s, capacity= float("inf") , t_time = 0)
            
    for s in N.S_minus:
        if s not in S:
            Graph.add_edge(s, "SINK", capacity= float("inf") , t_time = 0)
            
    
    
    return Graph
    
    

    
    
    
    

def extended_network_2(N_S, theta):
    # PRE: N: Network as outputted from extended_network_1, one source and one sink
    # , denotes by SOURCE and SINK     
    # POST: computes extended network 
    # as follows:
    #     -connect t to s with an arc of a_prime of infinite capacity 
    #         and transit time -theta
    G = N_S
    G.add_edge("SINK", "SOURCE", capacity= float("inf") , t_time = - theta)
    

    return G
    
    
    
    



def B(S: list, b : dict):
    # Pre : -> S : Subset of terminals
    # b -> dictionary of demands
    
    # Rerturns sum of demands of terminals in S
    res = 0
    
    for s in S:
        res += b[s]
    
    return res
    

def o(N, theta, S):
    #Pre :  N : Instance of problem, time hoirzon theta, subset of terminals S, 
    # computes maximum amount of flow over time that can be sent from sources 
    # S_plus inter. S to sinks S_minus w.o. S with time horizon theta
    #this maximum flow is equal to an classical max s-t flow over time problem
    #in the exptended network 1
    
    N_s = extended_network_1(N, S)
    return -Ford_Fulkerson(N_s, theta)
    
    #to solve max s-t flow over time problem we use ford and fulkerson algorithm
    
    
    
    
def d_theta_S(N, theta, S):
     # Computes the function $d^Theta(S)$, given : 
     #     -Instance of Quickest Transshipment Problem
     #     -Time horizon :  theta
     #     -Subset od Sources and Sinks : S passed as list !!!!
     #  PRE:  N : instance of problem, theta: time horizon, S, subset of terminals (given a a list)
     #  POST: computes the function d_theta_S, the aim of this script
     
         
    return o(N, theta,  S) - B(S, N.b)



# =============================================================================
# More testing
# =============================================================================


####  informative plots of d_theta(S)

# =============================================================================
# S = {"S_1", "S_2", "S_3", "S_4", "S_5"}
# 
# x = np.linspace(0, 18, 20)
# 
# 
# 
# y_1 = []
# y_2 = []
# y_3 = []
# y_4 = []
# y_5 = []
# y_6 = []
# y_7 = []
# 
# for i in x: y_1.append(d_theta_S(N, i, ["S_1"]))
# for i in x: y_2.append(d_theta_S(N, i, ["S_1", "S_2"] ))
# for i in x: y_3.append(d_theta_S(N, i, ["S_1", "S_2", "S_3"] ))
# for i in x: y_4.append(d_theta_S(N, i, ["S_2"] ))
# for i in x: y_5.append(d_theta_S(N, i, ["S_3"] ))
# for i in x: y_6.append(d_theta_S(N, i, ["S_3", "S_2"] ))
# for i in x: y_7.append(d_theta_S(N, i, ["S_1", "S_3"] ))
# 
# 
# 
# plt.figure(dpi = 800)
# plt.plot(x, y_1, label = "y_1")
# plt.plot(x, y_2, label = "y_2")
# plt.plot(x, y_3, label = "y_3")
# plt.plot(x, y_4, label = "y_4")
# plt.plot(x, y_5, label = "y_5")
# plt.plot(x, y_6, label = "y_6")
# plt.plot(x, y_7, label = "y_7")
# plt.legend()
# 
# =============================================================================


# =============================================================================
# S = [(0, 1), (0, 0)]
#  
# x = np.linspace(0, 40, 20)
# y = []
# 
# for i in x: y.append(d_theta_S(N, i, S_i))
# 
# plt.plot(x, y)
#     
# =============================================================================
