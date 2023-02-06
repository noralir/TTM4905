import matplotlib.pyplot as plt
import math
import numpy as np
import json
from readdatacsv import read_data_csv

def plotMM1(filename_input, filename_data):
    # --- THEORETICAL -------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    f = lambda l, x : l * math.e**(-l * x)
    plt.plot(
        np.arange(0, 100, 0.25), 
        f(1/input_variables["avg_pkt_ia_time_us"], np.arange(0, 100, 0.25)), 
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
    plt.title("MM1")
    plt.legend()
    plt.show()
    # ------------------------------------ #


#plotMM1(filename_input="01_MM1/MM1_input.json", filename_data="01_MM1/MM1_data/MM1_0_data.csv")
for i in [0, 10, 100, 1000, 10000]:
    plotMM1(filename_input="01_MM1/MM1_input.json", filename_data="01_MM1/nth_packet/" + str(i) + ".csv")