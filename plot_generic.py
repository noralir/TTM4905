import matplotlib.pyplot as plt
import math
import numpy as np
import json
import os
from readdatacsv import read_data_csv

waitMM1 = lambda u, l, t : 1 - l/u * math.e**(-(u-l)*t)
sojournMM1 = lambda u, l, t : (u-l) * math.e**(-(u-l)*t)
waitMD1 = lambda u, l, t : [((1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t]


def plot_gen(filename_input, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    
    lambda_list = [1/l for l in input_variables["avg_pkt_ia_time"]]
    mu_list = [1/((m/input_variables["capacity"])) for m in input_variables["avg_pkt_len_bits"]]
    x = np.arange(0, 150, 1)

    for i in range(len(lambda_list)):
        dist_type = input_variables["dist_type_pkt_ia_time"][i] + input_variables["dist_type_pkt_len"][i]
        if dist_type == "MM":
            y = waitMM1(mu_list[i], lambda_list[i], x)
        elif dist_type == "MD":
            y = waitMD1(mu_list[i], lambda_list[i], x)
            plt.yscale("log")
        plt.plot(x, y, label="theoretical #" + str(i) + " l = " + str(1/input_variables["avg_pkt_ia_time"][i]))
        
    


    #y = waitMD1(mu_, lambda_, x)
    #plt.plot(x, y, label="Theoretical distribution", color="blueviolet")

    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    num_pkts = input_variables["num_pkts"]
    fields_data, rows_data = read_data_csv(filename_data)
    
    #wait_rows = [row[2] for row in rows_data]
    
    i = 0
    #print((wait_rows))
    for n in num_pkts:
        test = rows_data[:n+1]
        rows_data = rows_data[n+1:]
        wait_hist, x_hist = np.histogram([t[2] for t in test], 100, density=True)
        plt.plot(x_hist[:-1], np.cumsum(wait_hist)/np.cumsum(wait_hist)[-1], label="run: " + str(i))
        #print([t[0] for t in test], len(test))
        #print([r[0] for r in rows_data], len(rows_data))
        i += 1

    delay = [row[2]+row[3] for row in rows_data]
    wait = [row[2] for row in rows_data]
    
    #wait_hist, x_hist = np.histogram(wait, 100, density=True)
    #plt.plot(x_hist[:-1], np.cumsum(wait_hist)/np.cumsum(wait_hist)[-1], label="sim_cumsum")
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    #plt.yscale("log")
    plt.xlabel("Time")
    plt.ylabel("P(T<=t)")
    #plt.xlim([0,5])
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #
    

plot_gen(filename_input="09_MM1-l/input.json", filename_data="09_MM1-l/data/0.csv")