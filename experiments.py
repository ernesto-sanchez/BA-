# -*- coding: utf-8 -*-
"""
Created on Sun May 29 18:52:09 2022

@author: SELISE
"""
"""
First we make a comparison between algo1 brute force and the using the minimizer for d_theta


"""
from generate_instances import problem
from algo_1 import algo1
from algorithm_1_brute_force import algo_1_bf
from algo_2 import algo2
from alg2_bf import algo2_bf
from tabulate import tabulate

import time


#### First we compare the time it takes to run both algorithms with different amounts of sources and sinks

#Average time to run algo 1 brute force with problem = 5, 0.2, 0.2, 10

av_time = 0
times_algo_1 = []
times_algo_1_bf = []
times_algo_2 = []
times_algo_2_bf = []

for i in range(10):
    
    N = problem( 5, 0.1, 0.1, 50)
# =============================================================================
#     start_time = time.time()
#     algo1(N)
#     times_algo_1.append(time.time() - start_time)
#     
#     start_time = time.time()
#     algo_1_bf(N)
#     times_algo_1_bf.append(time.time() - start_time)
# =============================================================================
    
    start_time = time.time()
    algo2(N)
    times_algo_2.append(time.time() - start_time)
    
    start_time = time.time()
    algo2_bf(N)
    times_algo_2_bf.append(time.time() - start_time)
    
    table = tabulate([times_algo_2, times_algo_2_bf], headers=['1', '2','3',' 4', '5', '6', '7',  '8', '9', '10'] )

    with open('results.txt', 'w') as f:
        f.write(table)
    

    
    