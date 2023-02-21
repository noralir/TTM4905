import matplotlib.pyplot as plt
import math
import numpy as np
import json
import scipy.stats as stats
import os
from readdatacsv import read_data_csv

def plotsojournMM1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : (u-l) * math.e**(-(u-l)*x) #sojourn time (eq 6.85 p172 ttm4110 book)
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))
    plt.plot(
        np.arange(0, 20000, 100), 
        f(mu_,lambda_, np.arange(0, 20000, 100)), 
        label="Theoretical distribution", 
        color="forestgreen"
    )
    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    print("start read data")
    fields_data, rows_data = read_data_csv(filename_data)
    print("end read data")
    print(rows_data.shape)
    print("start delay")
    delay = [row[2]+row[3] for row in rows_data]
    print("end delay")
    n, x, _ = plt.hist(delay, density=True, label="Simulation data", color='palegreen', bins=500)

    #test = stats.fit(delay)
    plt.plot(x[:-1], n, label="Simulation data", color="springgreen")
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("File: " + filename_data)
    plt.legend()
    plt.xlim([0, 20000])
    plt.show()
    # ------------------------------------ #

def plotwaitMM1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : 1 - l/u * math.e**(-(u-l)*x) #wait time (eq. 6.84 p 172 ttm4110 book)
    #f = lambda u, l, x : math.e**(-(u-l)*x) #wait time (eq. 6.84 p 172 ttm4110 book)
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))
    plt.plot(
        np.arange(0, 20000, 100), 
        f(mu_, lambda_, np.arange(0, 20000, 100)), 
        label="Theoretical distribution", 
        color="forestgreen"
    )
    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    fields_data, rows_data = read_data_csv(filename_data)
    wait = [row[2] for row in rows_data]
    plt.hist(wait, density=False, label="Simulation data", color='palegreen', bins=50)
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    plt.xlabel("Wait time")
    plt.ylabel("Probability")
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #


def plotnthMM1(filename_input, input_index, folder_nth):
    # --- NTH --------------------------- #
    for file in os.listdir(folder_nth):
        fields_data, rows_data = read_data_csv(folder_nth + file)
        delay = [row[2]+row[3] for row in rows_data]
        #n, x, _ = plt.hist(delay, density=True, label=file, bins=500)
        n, x = np.histogram(delay, 150, density=True)
        plt.plot(x[:-1], n, label=file)
    # ------------------------------------ #

    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda u, l, x : (u-l) * math.e**(-(u-l)*x) #sojourn time (eq 6.85 p172 ttm4110 book)
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))
    plt.plot(
        np.arange(0, 20000, 100), 
        f(mu_,lambda_, np.arange(0, 20000, 100)), 
        label="Theoretical distribution", 
        color="forestgreen"
    )
    # ------------------------------------ #

    # --- PLOT --------------------------- #
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("Folder: " + folder_nth)
    plt.legend()
    plt.xlim([0, 10000])
    plt.show()
    # ------------------------------------ #

#plotsojournMM1(filename_input="06_MM1/input.json", input_index=0, filename_data="06_MM1/data/0.csv")
#plotwaitMM1(filename_input="06_MM1/input.json", input_index=0, filename_data="06_MM1/data/1.csv")
plotnthMM1(filename_input="06_MM1/input.json", input_index=0, folder_nth="06_MM1/nth/0/")