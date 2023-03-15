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

    theoretical_plotted=[]
    for i in range(len(lambda_list)):
        dist_type = input_variables["dist_type_pkt_ia_time"][i] + input_variables["dist_type_pkt_len"][i]
        if dist_type == "MM":
            y = waitMM1(mu_list[i], lambda_list[i], x)
        elif dist_type == "MD":
            y = waitMD1(mu_list[i], lambda_list[i], x)
            plt.yscale("log")
        if lambda_list[i] not in theoretical_plotted:
            plt.plot(x, y, label="theoretical,  l = " + str(round(1/input_variables["avg_pkt_ia_time"][i], 3)))
            theoretical_plotted.append(lambda_list[i])

    # ------------------------------------ #

    # --- SIMULATION --------------------- #
    num_pkts = input_variables["num_pkts"]
    fields_data, rows_data = read_data_csv(filename_data)
    
    
    i = 0

    for n in num_pkts:
        test = rows_data[:n+1]
        rows_data = rows_data[n+1:]
        wait_hist, x_hist = np.histogram([t[2] for t in test], 100, density=True)
        plt.plot(x_hist[:-1], np.cumsum(wait_hist)/np.cumsum(wait_hist)[-1], label="run: " + str(i))
        i += 1

    delay = [row[2]+row[3] for row in rows_data]
    wait = [row[2] for row in rows_data]
    
    # ------------------------------------ #
    
    # --- PLOT --------------------------- #
    #plt.yscale("log")
    plt.xlabel("Time")
    plt.ylabel("P(T<=t)")
    plt.xlim([0,300])
    plt.title("File: " + filename_data)
    plt.legend()
    plt.show()
    # ------------------------------------ #
    

def plot_gen_nth(filename_input, folder_nth, indexes = [0]):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    avg_pkt_ia_time = input_variables["avg_pkt_ia_time"]

    

    f = lambda u, l, x : (u-l) * math.e**(-(u-l)*x) #sojourn time (eq 6.85 p172 ttm4110 book)


    t = np.arange(0, 150, 1)
    #plt.plot(t, f(mu_, lambda_, t), label="Theoretical distribution")

    fig, axs = plt.subplots(2, 3)

    theoretical_plotted = []
    for i in indexes:
        lambda_ = 1/input_variables["avg_pkt_ia_time"][i]
        mu_ = 1/((input_variables["avg_pkt_len_bits"][i]/input_variables["capacity"]))

        folder_nth_i = folder_nth + str(i) + "/"
        j=0

        files = os.listdir(folder_nth_i)
        files.sort()

        for file in files:
            ax_x, ax_y = math.floor(j/3) ,j%3

            #Theoretical#
            theoretical_plot = str(lambda_)+"_"+file
            if theoretical_plot not in theoretical_plotted:
                axs[ax_x, ax_y].plot(t, f(mu_, lambda_, t), label="lamdba="+str(round(lambda_, 3)))
                axs[ax_x, ax_y].set_title(file)
                axs[ax_x, ax_y].set_xlim([0,80])
                axs[ax_x, ax_y].set_xlabel("t")
                axs[ax_x, ax_y].set_ylabel("F_S(t)")

                theoretical_plotted.append(theoretical_plot)

            #Simulated#
            fields_data, rows_data = read_data_csv(folder_nth_i + file)
            delay = [row[2]+row[3] for row in rows_data]
            n, x = np.histogram(delay, 150, density=True)
            axs[ax_x, ax_y].plot(x[:-1], n, label=str(i)+"/"+file+", lamdba="+str(round(lambda_, 3)), ls="--")
            
            axs[ax_x, ax_y].legend()
            j+=1

    plt.show()


#plot_gen_nth(filename_input="09_MM1-l/input.json", folder_nth="09_MM1-l/nth/", indexes = [0,1,2,3,4])