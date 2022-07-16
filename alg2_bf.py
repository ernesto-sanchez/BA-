# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 15:41:38 2022

@author: SELISE
"""


from itertools import chain, combinations
from compute_d_theta_S import d_theta_S
from generate_instances import problem
from compute_cut_theta_S import cut_theta_S
import time
import math
from minimizer_d_theta import algo3




def powerset(seq):

    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
         
            
         
def argmin(N, theta):
    #Pre : Network instance N, tehta integer
    #Post: argmin and min (in that order) of d_theta(S) across all subsets of S_plus and S_minus
    
    
    curr_min =  float("inf")
    curr_argmin = 0
    
    accross = list(powerset(N.S_plus + N.S_minus))
    
    for i in accross:
        if d_theta_S(N, theta, i) < curr_min:
            curr_min = d_theta_S(N, theta, list(i))
            curr_argmin = i
            #print("curr_argmin is : " + str(i))
            
            
    return curr_argmin, curr_min


# =============================================================================
# def bin_search(N, S_i, t_0, t_1):
#     #PRE : Subset of terminals S_i, time interval for serching the zero
#     #POST : find Theta_i_prime usin binary search within the time interval [t_0, t_1]
#     
#     # we perform the binary search with accuracy of 0.1 units
#     #print("binsearch in : " + str(t_0) +"and " + str(t_1))
#     tol = 0.01
#     #time.sleep(0.5)
#     if d_theta_S(N, t_0, S_i) >= 0: return t_0
#     
#     # print("d_theta_s is :"  +  str(d_theta_S(N, t_0, S_i)))
#     #time.sleep(1)
#     
#     pivot =  t_0 + (t_1 - t_0)/2
#     
#     #print("pivot is: " + str(pivot))
#     #time.sleep(0.5)
#     
#     if  d_theta_S(N, pivot, S_i) > - tol and d_theta_S(N, pivot, S_i) < tol:
#         #print("pivot is right")
#         return pivot
#     
#     if d_theta_S(N, pivot, S_i) >= tol :
#        # print("pivot is bigger")
#         return bin_search(N, S_i, t_0, pivot)
#     if d_theta_S(N, pivot, S_i) <= -tol : 
#         #print("pivot is smaller")
#         return bin_search(N, S_i, pivot, t_1)
#     print("mistake in binsearch")
#     
#     pass
# =============================================================================

def bin_search_int(N, S_i, t_0, t_1):
    
    #print ("t_o =" + str(t_0) + "T_1 = " + str(t_1)) 
    if d_theta_S(N, t_0, S_i) > 0: return t_0
    if d_theta_S(N, t_1, S_i) > 0 and d_theta_S(N, t_1 - 1, S_i) < 0: return t_1
    
    pivot =  math.floor(t_0 + (t_1 - t_0)/2)
    
    if  d_theta_S(N, pivot, S_i)  > 0 and d_theta_S(N, pivot -1, S_i) <= 0:
        #print("pivot is right : " + str(pivot))
        return pivot
    
    if d_theta_S(N, pivot, S_i) > 0 and d_theta_S(N, pivot - 1, S_i) >0 :
        #print("pivot is bigger :   " + str(pivot))
        return bin_search_int(N, S_i, t_0, pivot)
    
    else : 
        #print("pivot is smaller:   " + str(pivot))
        return bin_search_int(N, S_i, pivot, t_1)
    print("mistake in binsearch")
    
 





def algo2_jap(N, S_i):
    if d_theta_S(N, 0, S_i) >= 0: return 0
    
    else: t = 1
    

    while d_theta_S(N, t, S_i) < 0:
        t = 2*t
    
    return bin_search_int(N, S_i, t/2, t)
    








def algo2_bf(N):
    # Pre: instance of Problem
    # Post: Minimum feasible time Horzon for the quickest transshipment
    
    
    #### Treat J as set. Should make things faster
    #start_time = time.time()
    J = set()
    theta_i = 0
    tol = 0.01  # For the bin search
    
    k = len(N.S_plus + N.S_minus)
    
    for i in range(math.ceil(math.log2((k**2)/4)) + 1):
        J.add(2**i)
    
    
    
    while True:
        
        S_i, d_theta_i = argmin(N, theta_i)
     
        
        #print("S_i: ", S_i, "d_theta: ", d_theta_i)
        #time.sleep(1)
    
        if d_theta_i < -tol:
            theta_i_prime = algo2_jap(N, S_i)
            
            thetas = set()
            thetas.add(theta_i_prime)
            
            for j in J:
                
                theta = theta_i_prime + ((j * (-d_theta_S(N, theta_i, argmin(N, theta_i_prime)[0])))/cut_theta_S(N, theta_i_prime, S_i))
                theta = round(theta)
                #print(str(theta) + " ____" + str(cut_theta_S(N, theta_i_prime, S_i)))
                
                                         
                if d_theta_S(N, theta, algo3(N, theta)) < 0:
                    
                   # print("appending a theta")
                    
                    thetas.add(theta)
                
                    
            theta_i = max(thetas)
            #print("new theta i is   " + str(theta_i) + "///" + str(d_theta_S(N, theta_i, algo3(N, theta_i))))
        
            
            #print("theta_i is : "+ str(theta_i))
        else: 
            #print("were breaking")
            #print("--- %s seconds ---" % (time.time() - start_time))

            return theta_i