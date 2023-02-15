import matplotlib.pyplot as plt
import math
import numpy as np
import json
from readdatacsv import read_data_csv

def plotsojournMM1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : (u-l) * math.e**(-(u-l)*x) #sojourn time (eq 6.85 p172 ttm4110 book)
    lambda_ = 1/input_variables["avg_pkt_ia_time_us"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity_bps"])*10**6)
    plt.plot(
        np.arange(0, 100, 0.25), 
        f(mu_,lambda_, np.arange(0, 100, 0.25)), 
        label="Theoretical distribution", 
        color="blueviolet"
    )
    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    fields_data, rows_data = read_data_csv(filename_data)
    delay = [row[2]+row[3] for row in rows_data]
    plt.hist(delay, density=True, label="Simulation data", color='aquamarine', bins=100)
    # ------------------------------------ #


    
    # --- PLOT --------------------------- #
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #

def plotwaitMM1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : 1 - l/u * math.e**(-(u-l)*x) #wait time (eq. 6.84 p 172 ttm4110 book)
    lambda_ = 1/input_variables["avg_pkt_ia_time_us"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity_bps"])*10**6)
    plt.plot(
        np.arange(0, 100, 0.25), 
        f(mu_, lambda_, np.arange(0, 100, 0.25)), 
        label="Theoretical distribution", 
        color="blueviolet"
    )
    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    fields_data, rows_data = read_data_csv(filename_data)
    wait = [row[2] for row in rows_data]
    plt.hist(wait, density=True, label="Simulation data", color='aquamarine', bins=100)
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    plt.xlabel("Wait time")
    plt.ylabel("Probability")
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #


plotsojournMM1(filename_input="05_MM1-MD1/input.json", input_index=0, filename_data="05_MM1-MD1/MM1/0.csv")
#plotwaitMM1(filename_input="05_MM1-MD1/input.json", input_index=0, filename_data="05_MM1-MD1/MM1/0.csv")
