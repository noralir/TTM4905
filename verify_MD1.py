import matplotlib.pyplot as plt
import math
import numpy as np
import json
import os
from readdatacsv import read_data_csv

def plotMD1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : u + l * math.e**(-l * x)
    plt.plot(
        np.arange(0, 10000, 100), 
        f(1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"])), 1/input_variables["avg_pkt_ia_time"][input_index], np.arange(0, 10000, 100)), 
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

def plotnthMD1(filename_input, input_index, folder_nth):
    # --- NTH --------------------------- #
    for file in os.listdir(folder_nth):
        if file != "0.csv":
            fields_data, rows_data = read_data_csv(folder_nth + file)
            delay = [row[2]+row[3] for row in rows_data]
            #n, x, _ = plt.hist(delay, density=True, label=file, bins=500)
            n, x = np.histogram(delay, 300, density=True)
            plt.plot(x[:-1], n, label=file)
    # ------------------------------------ #

    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : u + l * math.e**(-l * x)
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))
    plt.plot(
        np.arange(0, 10000, 100), 
        f(mu_,lambda_, np.arange(0, 10000, 100)), 
        label="Theoretical distribution", 
        color="forestgreen"
    )
    # ------------------------------------ #

    # --- PLOT --------------------------- #
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("Folder: " + folder_nth)
    plt.legend()
    plt.xlim([0, 2500])
    plt.show()
    # ------------------------------------ #


#plotMD1(filename_input="07_MD1/input.json", input_index=0, filename_data="07_MD1/data/0.csv")

plotnthMD1(filename_input="07_MD1/input.json", input_index=0, folder_nth="07_MD1/nth/0/")

