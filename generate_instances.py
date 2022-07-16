# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:18:13 2022

@author: Ernesto 
"""

# =============================================================================
# In this script we aim to generate intances to the quickest transshipment problem.
#  
# =============================================================================


# =============================================================================
# 
# The Network will be generated following these guidelines:
#     - The underlying Graph is an NxN Grid (N**2 nodes and 2*N*(N-1) edges)
#     - The sinks and sources are chosen randomly?
#     -   
#     - The amount ofsources and sinks are given by round (N^2 x S_plus) and round (N^2 x S_minus), where S_plus and S_minus are input paramenters in [0,1]
#         s.t. S_plus + S_minus < 1
#         
#     - For each arc, the capacity and transit time are chosen u.a.r from [10] and {1, ..., 10} respectively
#     - Supply and demand vectors  TODO
#         
#         
# =============================================================================

# =============================================================================
# 
# Approach : To be discussed#
# 
# Choose sources, sinks, capacitites and transit times ranrandomly
# ceate arcs in both ways because otherwise there is no guarantee that 
# the flow conditions are satisfied.
# 
# 
# =============================================================================






import networkx as nx
import matplotlib.pyplot as plt
import random
import math




class problem:
    
    
    
    G = nx.Graph()
    
    def __init__(self, N, S_plus, S_minus, US):
        
        self.N = N
        self.S_plus = S_plus
        self.S_minus = S_minus
        self.US = US
        
        self.G = nx.grid_graph([self.N, self.N])
        self.G = nx.DiGraph(self.G)
        
        
        self.S_plus = random.sample(list(self.G.nodes), math.floor((N**2)*S_plus))
        self.S_minus = random.sample(list(i for i in self.G.nodes if i not in self.S_plus), math.floor((N**2)*S_minus))
        
        # print(S_plus)
        # print(S_minus)
        
        # add attributes to the edges, and also add a position, convenient for plotting later on
        
        attrs_edge = {}   
        attrs_node = {}
        for edge in list(self.G.edges):
            attrs_edge[edge] = {"capacity": float(random.randint(1,10)), "t_time" : float(random.randint(1,10))}
        for node in list(self.G.nodes):
            attrs_node[node] = {"pos" : [node[0], node[1]]}
            
        #print(attrs)
        

        nx.set_edge_attributes(self.G, attrs_edge)
        nx.set_node_attributes(self.G, attrs_node)

         
        #supply and demand 
        
        
        self.b = {} 
        
        supplies = []
        demands = []
        
        for i in range(len(self.S_plus)):
            supplies.append(random.randint(0, US))
            
        tot_sup = sum(supplies)
            
        for i in range(len(self.S_minus) -1):
            dem = random.randint(0, tot_sup)
            demands.append(dem)
            tot_sup -= dem
        demands.append(tot_sup)
    
        
        # print(supplies)
        # print(demands)
        assert sum(supplies) == sum(demands)
        
        for source in self.S_plus:
            self.b[source] = supplies.pop()
            
        for sink in self.S_minus:
            self.b[sink] = -demands.pop()
            
  
        


    
# =============================================================================
#         pos = nx.spring_layout(self.G, seed = 1288)
# 
#         nx.draw_networkx(self.G,pos , with_labels=True,font_size = 6, arrows = True)
#         nx.draw_networkx_nodes(self.G, pos, nodelist= self.S_minus, node_color="tab:red")
#         nx.draw_networkx_nodes(self.G, pos, nodelist= self.S_plus, node_color="tab:green")
# 
# =============================================================================
                
        
        

    
    
        
        
        
        
    
    
    #SOME TESTING
    
# =============================================================================
# H = problem(4, 0.15, 0.35, 33)
# 
#         
#         
# pos = nx.spring_layout(H.G, seed = 1288)
# 
# plt.figure(dpi = 1200)
# nx.draw_networkx(H.G,pos , with_labels=True,font_size = 6, arrows = True)
# nx.draw_networkx_nodes(H.G, pos, nodelist= H.S_minus, node_color="tab:red")
# nx.draw_networkx_nodes(H.G, pos, nodelist=H.S_plus, node_color="tab:green")
# 
#         
#         
# =============================================================================
        
        
        
    