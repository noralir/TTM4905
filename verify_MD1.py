import matplotlib.pyplot as plt
import math
import numpy as np
import json
import os
from readdatacsv import read_data_csv

waitMD1 = lambda u, l, t : [((1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t]

def plotMD1(filename_input, input_index, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    #f = lambda u, l, x : u + l * math.e**(-l * x)
    x = np.arange(0, 10, 1)

    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]

    y = waitMD1(mu_, lambda_, x)
    plt.plot(x, y, label="Theoretical distribution", color="blueviolet")

    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    fields_data, rows_data = read_data_csv(filename_data)
    delay = [row[2]+row[3] for row in rows_data]
    wait = [row[2] for row in rows_data]
    wait_hist, x_hist = np.histogram(wait, 100, density=True)
    plt.plot(x_hist[:-1], np.cumsum(wait_hist)/np.cumsum(wait_hist)[-1], label="sim_cumsum")
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    plt.yscale("log")
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.xlim([0,5])
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #

def plotnthMD1(filename_input, input_index, folder_nth):
    # --- NTH --------------------------- #
    for file in os.listdir(folder_nth):
        fields_data, rows_data = read_data_csv(folder_nth + file)
        delay = [row[2]+row[3] for row in rows_data]
        wait = [row[2] for row in rows_data]
        #n, x, _ = plt.hist(delay, density=True, label=file, bins=500)
        n, x = np.histogram(wait, 200, density=True)
        plt.plot(x[:-1], n, label=file)
    # ------------------------------------ #

    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    #f = lambda u, l, x : u + l * math.e**(-l * x)
    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/((input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"]))

    t = np.arange(0, 10000, 100)
    y = waitMD1(mu_, lambda_, t)
    plt.plot(t, y, label="Theoretical distribution", color="forestgreen")
    # ------------------------------------ #

    # --- PLOT --------------------------- #
    plt.yscale("log")
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("Folder: " + folder_nth)
    plt.legend()
    plt.xlim([0, 10000])
    plt.show()
    # ------------------------------------ #

def plottheoreticalMD1(filename_input, input_index=0):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    lambda_ = 1/input_variables["avg_pkt_ia_time"][input_index]
    mu_ = 1/(input_variables["avg_pkt_len_bits"][input_index]/input_variables["capacity"])

    x = np.arange(0, 20, 1)
    y = waitMD1(mu_, lambda_, x)
    plt.plot(x, y, label="meh")

    #plt.yscale("log")
    plt.xlabel("Sojourn time")
    plt.ylabel("Probability")
    plt.title("File: " + filename_input)
    plt.legend()
    #plt.xlim([0, 10000])
    plt.show()
   

#------------------------------------ RUN ------------------------------------#
#plotMD1(filename_input="07_MD1/input.json", input_index=0, filename_data="07_MD1/data/0.csv")
#plotnthMD1(filename_input="07_MD1/input.json", input_index=0, folder_nth="07_MD1/nth/0/")
plottheoreticalMD1(filename_input="08_MD1/input.json")
