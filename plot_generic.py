import matplotlib.pyplot as plt
import math
import numpy as np
import json
import os
from readdatacsv import read_data_csv

wait_pdf_MM1 = lambda u, l, t : False #TODO
wait_cdf_MM1 = lambda u, l, t : 1 - l/u * math.e**(-(u-l)*t) 
sojourn_pdf_MM1 = lambda u, l, t : (u-l) * math.e**(-(u-l)*t) 
sojourn_cdf_MM1 = lambda u, l, t : False #TODO

wait_pdf_MD1 = lambda u, l, t : False #TODO
wait_cdf_MD1 = lambda u, l, t : [((1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t]
sojourn_pdf_MD1 = lambda u, l, t : False #TODO
sojourn_cdf_MD1 = lambda u, l, t : False #TODO

sojourn_MD1_not_working = lambda u, l, t : [( (1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t] #TODO: not working

def MG1(u, l, S2, t):
    return False

def get_y_theoretical(u, l, t, dist_type, plot_type, S2=0):
    # --- M/M/1 ----------------------------------------- #
    if dist_type == "MM" and plot_type == "wait_cdf":
        return wait_cdf_MM1(u, l, t)
    elif dist_type == "MM" and plot_type == "wait_pdf":
        return wait_pdf_MM1(u, l, t)
    elif dist_type == "MM" and plot_type == "sojourn_cdf":
        return sojourn_cdf_MM1(u, l, t)
    elif dist_type == "MM" and plot_type == "sojourn_pdf":
        return sojourn_pdf_MM1(u, l, t)
    # --------------------------------------------------- #
    # --- M/D/1 ----------------------------------------- #
    elif dist_type == "MD" and plot_type == "wait_cdf":
        return wait_cdf_MD1(u, l, t)
    elif dist_type == "MD" and plot_type == "wait_pdf":
        return wait_pdf_MD1(u, l, t)
    elif dist_type == "MD" and plot_type == "sojourn_cdf":
        return sojourn_cdf_MD1(u, l, t)
    elif dist_type == "MD" and plot_type == "sojourn_pdf":
        return sojourn_pdf_MD1(u, l, t)
    # --------------------------------------------------- #
    # --- X/G/1 ----------------------------------------- #
    elif "MG" in dist_type:
        return MG1(u, l, t)
    # --------------------------------------------------- #

    return False

def get_x_y_simulation(rows_data, plot_type):
    hist, x_hist = [], []
    if "wait" in plot_type:
        wait = [row[2] for row in rows_data]
        hist, x_hist = np.histogram(wait, 100, density=True)
    elif "sojourn" in plot_type:
        delay = [row[2]+row[3] for row in rows_data]
        hist, x_hist = np.histogram(delay, 100, density=True)
    if "cdf" in plot_type:
        return x_hist[:-1], np.cumsum(hist)/np.cumsum(hist)[-1]
    elif "pdf" in plot_type:
        return x_hist[:-1], hist

def get_theoretical_list_flattened(list, wanted_type):
    return_list = []
    for item in list:
        if type(item) == wanted_type:
            return_list.append(item)
        elif type(item) == type([]):
            for subitem in item:
                return_list.append(item) 
    return return_list


def plot_gen_file(filename_input, filename_data, plot_type="wait_cdf"):
    # --- THEORETICAL --------------------------------------------------------------------------------------------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    '''
    
    #HANDLE IF NUM SOURCES#
    if "num_sources" in input_variables: # If multiple soruces (with priority)
        num_sources = input_variables["num_sources"]
        for i in range(len(num_sources)):
            dist_type_pkt_ia_time_i = input_variables["dist_type_pkt_ia_time"][i]
            if type(dist_type_pkt_ia_time_i) == type([]):
                dist_type_pkt_ia_time_i = "G"
            dist_type_pkt_len_i = input_variables["dist_type_pkt_len"][i]
            if type(dist_type_pkt_len_i) == type([]):
                dist_type_pkt_len_i = "G"
            dist_type = dist_type_pkt_ia_time_i + dist_type_pkt_len_i

            lambda_i = [1/t for t in input_variables["avg_pkt_ia_time"][i]]
            mu_i = [1/t for t in input_variables["avg_pkt_len_bits"][i]]
            
            t = np.arange(0, 150, 1)
            y = get_y_theoretical(mu_i, lambda_i, t, dist_type, plot_type, S2=input_variables["variance_pkt_len_bits"][i])

    '''



    lambda_list = [1/l for l in input_variables["avg_pkt_ia_time"]] # Get lambdas
    mu_list = [1/((m/input_variables["capacity"])) for m in input_variables["avg_pkt_len_bits"]] # Get mus
    t = np.arange(0, 150, 1)
    theoretical_plotted=[] # Handle if plots have been done already
    for i in range(len(lambda_list)):
        dist_type = input_variables["dist_type_pkt_ia_time"][i] + input_variables["dist_type_pkt_len"][i] #e.g. "MM"
        y = get_y_theoretical(mu_list[i], lambda_list[i], t, dist_type, plot_type)
        if dist_type == "MD":
            plt.yscale("log")
        plotted_dist = dist_type+str(lambda_list[i])+str(mu_list[i])
        if plotted_dist not in theoretical_plotted:
            theoretical_plotted.append(plotted_dist) #Only plot if not already plotted
            if type(y) == type(np.array([])): #Only plot if dist is implemented
                plt.plot(t, 
                        y, 
                        label="theoretical,  l = " + str(round(lambda_list[i], 3))+", mu="+str(round(mu_list[i],3))) 
    # ------------------------------------------------------------------------------------------------------------------------- #
    # --- SIMULATION ---------------------------------------------------------------------------------------------------------- #
    num_pkts = input_variables["num_pkts"]
    fields_data, rows_data = read_data_csv(filename_data)
    i = 0
    for n in num_pkts:
        test = rows_data[:n+1]
        rows_data = rows_data[n+1:]
        plot_x, plot_y = get_x_y_simulation(test, plot_type)
        plt.plot(plot_x, 
                 plot_y, 
                 label="run: " + str(i) +", lambda="+str(round(lambda_list[i], 3))+", mu="+str(round(mu_list[i],3)), 
                 ls="--")
        i += 1
    # ------------------------------------------------------------------------------------------------------------------------- #
    # --- PLOT ---------------------------------------------------------------------------------------------------------------- #
    plt.xlabel("Time")
    plt.ylabel("P(T<=t)")
    #plt.xlim([0,80]) #TODO: make dependant on whats beeing plotted
    plt.title("File: " + filename_data +", type: "+plot_type)
    plt.legend()
    plt.show()
    # ------------------------------------------------------------------------------------------------------------------------- #
    
def plot_gen_nth(filename_input, folder_nth, indexes = [0], plot_type = "wait"):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    t = np.arange(0, 150, 1)
    fig, axs = plt.subplots(2, 3)
    theoretical_plotted = []
    for i in indexes:
        dist_type = input_variables["dist_type_pkt_ia_time"][i] + input_variables["dist_type_pkt_len"][i] #e.g. "MM"
        lambda_ = 1/input_variables["avg_pkt_ia_time"][i]
        mu_ = 1/((input_variables["avg_pkt_len_bits"][i]/input_variables["capacity"]))
        folder_nth_i = folder_nth + str(i) + "/"
        j=0
        files = os.listdir(folder_nth_i)
        files.sort()
        for file in files:
            ax_x, ax_y = math.floor(j/3) ,j%3
            # --- THEORETICAL ----------------------------------------------------------------------------------------------- #
            theoretical_plot = dist_type+str(lambda_)+"_"+file
            if theoretical_plot not in theoretical_plotted:
                y = get_y_theoretical(mu_, lambda_, t, dist_type, plot_type)
                if dist_type == "MM":
                    axs[ax_x, ax_y].set_ylabel("F_S(t)")
                elif dist_type == "MD":
                    axs[ax_x, ax_y].set_yscale("log")
                if type(y) == type(np.array([])):
                    axs[ax_x, ax_y].plot(t, y, label="lamdba="+str(round(lambda_, 3))+", mu="+str(round(mu_,3)))
                axs[ax_x, ax_y].set_title(file)
                #axs[ax_x, ax_y].set_xlim([0,80])
                axs[ax_x, ax_y].set_xlabel("t")
                theoretical_plotted.append(theoretical_plot)
            # --------------------------------------------------------------------------------------------------------------- #
            # --- SIMULATED ------------------------------------------------------------------------------------------------- #
            fields_data, rows_data = read_data_csv(folder_nth_i + file)
            plot_x, plot_y = get_x_y_simulation(rows_data, plot_type)
            axs[ax_x, ax_y].plot(plot_x, 
                                 plot_y, 
                                 label=str(i)+"/"+file+", lamdba="+str(round(lambda_, 3))+", mu="+str(round(mu_,3)), ls="--")
            # --------------------------------------------------------------------------------------------------------------- #
            axs[ax_x, ax_y].legend()
            j+=1
    plt.suptitle(plot_type+" time for "+folder_nth)
    plt.show()


def plot_MG1_priority_file(filename_input, filename_data):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    # THEORETICAL #
    m = 0
    # ----------- #
    # SIMULATION #
    fields_data, rows_data = read_data_csv(filename_data)
    i = 0
    num_pkts = input_variables["num_pkts"]
    for num_pkts_sublist in num_pkts:
        # n is list
        n = sum(num_pkts_sublist)
        part_of_dataset = rows_data[:n+1] # past of dataset that we are interested in for now
        rows_data = rows_data[n+1:] # Leftover data
        split = [[] for n in range(len(num_pkts_sublist))]

        for row in part_of_dataset:
            subindex = int(row[0][0])
            split[subindex].append(row)
        for list in split:

            plot_x, plot_y = get_x_y_simulation(list, "wait_pdf")

            plt.plot(plot_x, 
                    plot_y, 
                    label="test"+str(i), 
                    ls="--")
        i += 1
    # ---------- #
    # PLOT #
    plt.xlabel("Time")
    plt.ylabel("P(T<=t)")
    #plt.xlim([0,80]) #TODO: make dependant on whats beeing plotted
    plt.title("File: " + filename_data +", type: wait_pdf")
    plt.legend()
    plt.show()
    # ---- #