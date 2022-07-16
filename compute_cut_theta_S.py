# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:43:01 2022

@author: Ernesto Sanchez Tejedor
"""
# =============================================================================
# 
# Here we compute the function cut_theta_S as defined in the paper. 
# Dut_theta_S(S) is defined as the left hand side derivative of d_theta_S(S) as a function of theta.
#
# Cut_theta_S(S can be computed via a mincost circulation in the extended Network N(S, theta - epsilon, for infinitesimally small epsilon ))
# 
# =============================================================================
from generate_instances import problem
import networkx as nx
import sys
import numpy as np
import matplotlib.pyplot as plt

epsilon=sys.float_info.epsilon



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


    

def cut_theta_S(N, theta, S):
    #PRE: N instance of the problem, theta positive float, S subset of terminals
    #POST: left hnad derivative of d_theta_S(S) at theta
    
    N_1 = extended_network_1(N, S)
    dx = 0.0001
    dy = - Ford_Fulkerson(N_1, theta) + Ford_Fulkerson(N_1, theta - dx)
    
    
    return dy/dx
    
     



# =============================================================================
# 
# 
# x = np.linspace(0, 18, 200)
# y = []
#  
# for i in x: y.append(cut_theta_S(N, i, S))
#  
# plt.plot(x, y)
# =============================================================================
    
    