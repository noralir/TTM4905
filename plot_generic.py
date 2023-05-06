import matplotlib.pyplot as plt
import math
import numpy as np
import json
import os
from readdatacsv import read_data_csv

''' Comments
# * one
# ! two
# ? three
# TODO four
'''

def add_colors_to_plot():
    cl3 = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f']
    cl4 = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#f781bf','#a65628'] #! Good
    cl5 = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02'] #! Good
    cl6 = ['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cl4)

    ax = plt.axes()
    ax.set_facecolor("#fffcf5")

wait_pdf_MM1 = lambda u, l, t : False #TODO
wait_cdf_MM1 = lambda u, l, t : 1 - l/u * math.e**(-(u-l)*t) 
sojourn_pdf_MM1 = lambda u, l, t : (u-l) * math.e**(-(u-l)*t) 
sojourn_cdf_MM1 = lambda u, l, t : False #TODO



wait_pdf_MD1 = lambda u, l, t : [(1-(1-l/u)*sum([((((l/u)*k-l*t_)**k)/(math.factorial(k))*(math.e**(-((l/u)*k-l*t_)))) for k in range(math.floor(t_)+1)])) for t_ in t]
wait_cdf_MD1 = lambda u, l, t : [((1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t]
sojourn_pdf_MD1 = lambda u, l, t : False #TODO
sojourn_cdf_MD1 = lambda u, l, t : False #TODO

sojourn_MD1_not_working = lambda u, l, t : [( (1-l) * sum( [((l*(j-t_))**j) / (math.factorial(j)) * (math.e**(-l*(j-t_))) for j in range(math.floor(t_) + 1)] )) for t_ in t] #TODO: not working

def wait_pdf_GG1(u, l, t, sigma_squared_pkt_ia_time, sigma_squared_pkt_len):
    #! G/G/1 SINGLE CLASS 
    s_a = sigma_squared_pkt_ia_time # variance ia time
    s_s = sigma_squared_pkt_len # variance service time
    r = l/u #rho
    W_bar = (l * (r**2 + l**2 * s_s) * (s_a + s_s)) / (2 * (1-r) * (1 + l**2 * s_s))
    P_W_i_greater_than_t = lambda t : r*math.e**(-r*t/W_bar)
    return P_W_i_greater_than_t(t)

def get_y_theoretical(u, l, t, dist_type, plot_type, sigma_squared_pkt_ia_time=0, sigma_squared_pkt_len=0):
    #! Get theoretical distribution for single class
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
    elif dist_type == "MG":
        return False #TODO
    elif dist_type == "GG" and plot_type == "wait_pdf":
        return wait_pdf_GG1(u, l, t, sigma_squared_pkt_ia_time, sigma_squared_pkt_len)
    # --------------------------------------------------- #
    return False

def get_x_y_simulation(rows_data, plot_type):
    #! get x and y lists from silulation
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

def plot_gen_file(filename_input, filename_data, plot_type="wait_cdf"):
    #! SINGLE CLASS
    #! Only use for files consisting of one class (could be used for files with priority, but will not differentiate between them)
    #! Gives one plot with simulated values of specific plot type and theoretical one if it is implemeted, if distribution is changed over time the plots will lay on top of each other
    add_colors_to_plot()
    # --- THEORETICAL --------------------------------------------------------------------------------------------------------- #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    lambda_list = [1/l for l in input_variables["avg_pkt_ia_time"]] # Get lambdas
    sigma_squared_pkt_ia_time_list = input_variables["sigma_squared_pkt_ia_time"] if "sigma_squared_pkt_ia_time" in input_variables else 0
    mu_list = [1/((m/input_variables["capacity"])) for m in input_variables["avg_pkt_len_bits"]] # Get mus
    sigma_squared_pkt_len_list = input_variables["sigma_squared_pkt_len"] if "sigma_squared_pkt_len" in input_variables else 0
    t = np.arange(0, 150, 1)
    theoretical_plotted=[] # Handle if plots have been done already
    for i in range(len(lambda_list)):
        dist_type = input_variables["dist_type_pkt_ia_time"][i][0] + input_variables["dist_type_pkt_len"][i][0] #e.g. "MM"
        y = get_y_theoretical(mu_list[i], 
                              lambda_list[i], 
                              t, 
                              dist_type, 
                              plot_type, 
                              sigma_squared_pkt_ia_time_list[i] if type(sigma_squared_pkt_ia_time_list)==type([]) else 0,
                              sigma_squared_pkt_len_list[i] if type(sigma_squared_pkt_len_list)==type([]) else 0)
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
    #plt.xlim([0,80]) #TODO: make dependant on what's beeing plotted
    plt.title("File: " + filename_data +", type: "+plot_type)
    plt.legend()
    plt.show()
    # ------------------------------------------------------------------------------------------------------------------------- #
    
def plot_gen_nth(filename_input, folder_nth, indexes = [0], plot_type = "wait"):
    #! plot specific folder
    #! gives a plot with multiple subplots each showing packet n
    #add_colors_to_plot()
    # SINGLE CLASS #
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    t = np.arange(0, 150, 1)
    fig, axs = plt.subplots(2, 3)
    theoretical_plotted = []
    for i in indexes:
        dist_type = input_variables["dist_type_pkt_ia_time"][i][0] + input_variables["dist_type_pkt_len"][i][0] #e.g. "MM"
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

def MG1_priority_theoretical(class_i, lambda_,  mu_, sigma_squared_pkt_len):
    #! gives theoretical plots needed for plot_MG1_priority_file()
    rho_ = [lambda_[o]/mu_[o] for o in range(len(lambda_))]
    R_bar = sum([(rho_[j-1]**2 + lambda_[j-1]**2*sigma_squared_pkt_len[j-1])/(2*lambda_[j-1]) for j in class_i]) # one number, part of eq 13
    W_bar_i = lambda i : R_bar/((1-sum([rho_[j-1] for j in range(1,i)]))*(1-sum([rho_[j-1] for j in range(1, i+1)])))
    P_W_i_greater_than_t = lambda i, t : sum(rho_)*math.e**(-sum(rho_)*t/W_bar_i(i))

    t = np.arange(0,100,1)
    for ii in class_i:
        plt.plot(t, P_W_i_greater_than_t(ii, t), label=str(ii))

def GG1_priority_theoretical(class_i, lambda_, sigma_squared_pkt_ia_time, mu_, sigma_squared_pkt_len, W_bar_i):
    rho_ = [lambda_[o]/mu_[o] for o in range(len(lambda_))]
    P_W_i_greater_than_t = lambda i, t : sum(rho_)*math.e**(-sum(rho_)*t/W_bar_i[i-1])
    t = np.arange(0,100,1)
    for ii in class_i:
        plt.plot(t, P_W_i_greater_than_t(ii, t), label=str(ii))

def plot_priority_file(filename_input, filename_data):
    add_colors_to_plot()
    fields_data, rows_data = read_data_csv(filename_data)
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    # ----------------------------- SIMULATION ----------------------------- #
    
    i = 0
    num_pkts = input_variables["num_pkts"]
    for num_pkts_sublist in num_pkts:
        # n is list
        n = sum(num_pkts_sublist)
        part_of_dataset = rows_data[:n+1] # past of dataset that we are interested in for now
        rows_data = rows_data[n+1:] # Leftover data
        split = [[] for n in range(len(num_pkts_sublist))] # Split data based on 

        for row in part_of_dataset:
            str_number = str(int(row[0]))
            if len(str_number) == 1:
                str_number = "00"+str_number
            elif len(str_number) == 2:
                str_number = "0" + str_number
            subindex = int(str_number[-2])
            split[subindex].append(row)

        for j in range(len(split)):
            list = split[j]
            str_number = str(int(list[20][0]))
            pri = str_number[-1]
            #print("simulated average wait time of class",j+1, np.average([l[2] for l in list]))
            #print("-------------------------------------AVG PKT SIZE",np.average([l[4] for l in list]))
            plot_x, plot_y = get_x_y_simulation(list, "wait_pdf")
            plt.plot(plot_x, plot_y, label="subindex"+str(j)+", priority: "+pri+" sim part "+str(i), ls="--")
        i += 1
    # ---------------------------------------------------------------- #

    # ----------------------------- THEORETICAL ----------------------------- #
    for i in range(len(input_variables["num_sources"])):
        class_i = input_variables["num_sources"][i]
        lambda_ = [1/l for l in input_variables["avg_pkt_ia_time"][i]]
        sigma_squared_pkt_ia_time = input_variables["sigma_squared_pkt_ia_time"] if "sigma_squared_pkt_ia_time" in input_variables else False

        mu_ = [1/u for u in input_variables["avg_pkt_len_bits"][i]]
        sigma_squared_pkt_len = input_variables["sigma_squared_pkt_len"][i]

        dist_type_pkt_ia_time = input_variables["dist_type_pkt_ia_time"]
        if type(dist_type_pkt_ia_time) == type("M"):
            if dist_type_pkt_ia_time == "M":
                MG1_priority_theoretical(class_i, lambda_, mu_, sigma_squared_pkt_len) # Plots all classes
        elif type(dist_type_pkt_ia_time) == type([]):
            W_bar_i = [np.average([item[2] for item in l]) for l in split] # Gather W_bar_i
            GG1_priority_theoretical(class_i, lambda_, sigma_squared_pkt_ia_time, mu_, sigma_squared_pkt_len, W_bar_i)

    # ---------------------------------------------------------------------- #
    # ----------------------------- PLOT ----------------------------- #
    plt.xlabel("Time")
    plt.ylabel("P(T<=t)")
    plt.xlim([0,100]) #TODO: make dependant on whats beeing plotted
    plt.title("File: " + filename_data +", type: wait_pdf")
    plt.legend()
    plt.show()
    # ---------------------------------------------------------------- #

def plot_wait_times(filename_input, filename_data):
    #! plot all wait times from simulation
    #! add theoretical upper bound

    add_colors_to_plot()

    fields_data, rows_data = read_data_csv(filename_data)
    #t = [r[1] for r in rows_data]
    #t_buffer = [r[2] for r in rows_data] # With zeros
    t = [r[1] for r in rows_data if r[2] > 0]
    t_buffer = [r[2] for r in rows_data if r[2] > 0]
    plt.plot(t, t_buffer, '.')

    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    lambda_list = [1/l for l in input_variables["avg_pkt_ia_time"]]
    s_a_list = input_variables["sigma_squared_pkt_ia_time"] if "sigma_squared_pkt_ia_time" in input_variables else False
    mu_list = [1/u for u in input_variables["avg_pkt_len_bits"]]
    s_s_list = input_variables["sigma_squared_pkt_len"] if "sigma_squared_pkt_len" in input_variables else False

    dist_type_list = [input_variables["dist_type_pkt_ia_time"][i][0] + input_variables["dist_type_pkt_len"][i][0] for i in range(len(lambda_list))]

    '''
    #! the upper bound is for the averege wait time, not individual wait times
    for i in range(len(lambda_list)):
        W_upper_bound = False
        if dist_type_list[i] == "GG":
            l = lambda_list[i]
            s_a = s_a_list[i]
            s_s = s_s_list[i]
            r = lambda_list[i]/mu_list[i]
            W_upper_bound = (l * (s_a+s_s)) / (2 * (1-r))
            print(W_upper_bound)
        elif dist_type_list[i] == "MM":
            W_upper_bound = False
        if W_upper_bound:
            plt.plot(t, [W_upper_bound] * len(t))
    '''
    plt.show()

def plot_multiple_sources_no_priority(filename_input, filename_data, plot_type="wait_pdf", dist_type = "MM"):
    add_colors_to_plot()
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    all_lambdas_list = [[1/l for l in sublist] for sublist in input_variables["avg_pkt_ia_time"]]   
    lambda_list = [sum(sublist) for sublist in all_lambdas_list]



    avg_pkt_len_bits = input_variables["avg_pkt_len_bits"]



    avg_avg_pkt_len_bits_list = [np.average(b) for b in input_variables["avg_pkt_len_bits"]]
    mu_list = [1/t for t in avg_avg_pkt_len_bits_list]

    #SIM
    num_pkts = [sum(n) for n in input_variables["num_pkts"]]
    fields_data, rows_data = read_data_csv(filename_data)

    for i in range(len(all_lambdas_list)):
        highest_lambda = max(all_lambdas_list[i])
        index_of_highest_lambda = all_lambdas_list[i].index(highest_lambda)
        packets_highest = input_variables["num_pkts"][i][index_of_highest_lambda]
        priority_level_highest = input_variables["num_sources"][i][index_of_highest_lambda]
        packet_number_start = int(str(packets_highest)+str(index_of_highest_lambda)+str(priority_level_highest))

        lowest_lambda = min(all_lambdas_list[i])
        index_of_lowest_lambda = all_lambdas_list[i].index(lowest_lambda)
        packets_lowest = input_variables["num_pkts"][i][index_of_lowest_lambda]
        priority_level_lowest = input_variables["num_sources"][i][index_of_lowest_lambda]
        packet_number_stop = int(str(packets_lowest)+str(index_of_lowest_lambda)+str(priority_level_lowest))

        row_start = np.where(rows_data[:,0] == packet_number_start)[0][0]
        row_stop = np.where(rows_data[:,0] == packet_number_stop)[0][0]

        sim_lambda = 1/np.average([rows_data[:row_start][i+1]-rows_data[:row_start][i] for i in range(len(rows_data[:row_start])-1)])
        sim_mu = 1/np.average([r[4] for r in rows_data[:row_start]])
        print("sim l and u", sim_lambda, sim_mu)


        plot_x, plot_y = get_x_y_simulation(rows_data[:row_start], plot_type)
        plt.plot(plot_x, plot_y, label="sim", ls="--")
        rows_data = rows_data[row_stop+1:]


    #Theoretical 
    t = np.arange(0, 40, 1)
    for i in range(len(lambda_list)):
        print(lambda_list[i], mu_list[i])
        y = get_y_theoretical(mu_list[i], lambda_list[i], t, dist_type, plot_type)
        
        if type(y) == type(np.array([])) or type(y) == type([]):
            plt.plot(t,y,label="theoretical")
                      

    plt.legend()
    plt.show()

def plot_multiple_sources_with_priority(filename_input, filename_data, plot_type="wait_pdf"):

    add_colors_to_plot()

    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    num_pkts = input_variables["num_pkts"]
    num_sources = input_variables["num_sources"]
    priority_classes = [list(set(sublist)) for sublist in num_sources] # e.g. [1,2,3]
    #SIM--------------------------------------------------------------------------
    fields_data, rows_data = read_data_csv(filename_data)

    all_lambdas_list = [[1/l for l in sublist] for sublist in input_variables["avg_pkt_ia_time"]]
    #lambda_list = [sum(sublist) for sublist in all_lambdas_list]


    all_avg_pkt_len_bits = input_variables["avg_pkt_len_bits"]
    avg_avg_pkt_len_bits_list = [np.average(b) for b in input_variables["avg_pkt_len_bits"]]
    #mu_list = [1/t for t in avg_avg_pkt_len_bits_list]

    big_split = []
    for i in range(len(all_lambdas_list)):
        highest_lambda = max(all_lambdas_list[i])
        index_of_highest_lambda = all_lambdas_list[i].index(highest_lambda)
        packets_highest = input_variables["num_pkts"][i][index_of_highest_lambda]
        priority_level_highest = input_variables["num_sources"][i][index_of_highest_lambda]
        packet_number_start = int(str(packets_highest)+str(index_of_highest_lambda)+str(priority_level_highest))

        lowest_lambda = min(all_lambdas_list[i])
        index_of_lowest_lambda = all_lambdas_list[i].index(lowest_lambda)
        packets_lowest = input_variables["num_pkts"][i][index_of_lowest_lambda]
        priority_level_lowest = input_variables["num_sources"][i][index_of_lowest_lambda]
        packet_number_stop = int(str(packets_lowest)+str(index_of_lowest_lambda)+str(priority_level_lowest))

        row_start = np.where(rows_data[:,0] == packet_number_start)[0][0]
        row_stop = np.where(rows_data[:,0] == packet_number_stop)[0][0]

        part_of_dataset = rows_data[:row_start]
        rows_data = rows_data[row_stop+1:]

        split = [[] for n in range(len(priority_classes[i]))]
        for row in part_of_dataset:
            str_number = str(int(row[0]))
            subindex = int(str_number[-1])
            split[subindex-1].append(row)
        for j in range(len(split)):
            list_test = split[j]
            str_number = str(int(list_test[20][0]))
            pri = str_number[-1]
            plot_x, plot_y = get_x_y_simulation(list_test, plot_type)
            plt.plot(plot_x, plot_y, label="subindex"+str(j)+", priority: "+pri+" sim part "+str(i), ls="--")
        big_split.append(split)

    #-----------------------------------------------------------------------

    #THEORETICAL----------------------------------------------------------------
    '''
    lambda_list = [[1/l for l in sublist] for sublist in input_variables["avg_pkt_ia_time"]]
    mu_list = [[1/m for m in sublist] for sublist in input_variables["avg_pkt_len_bits"]]

    '''
    split_lambda_list = [[[] for s in sub] for sub in  priority_classes]
    split_mu_list = [[[] for s in sub] for sub in  priority_classes]

    for i in range(len(all_lambdas_list)):
        for j in range(len(all_lambdas_list[i])):
            split_lambda_list[i][num_sources[i][j]-1].append(all_lambdas_list[i][j])
            split_mu_list[i][num_sources[i][j]-1].append(all_avg_pkt_len_bits[i][j])

    lambda_i = [[sum(l) for l in sublist] for sublist in split_lambda_list]
    mu_i = [[1/np.average(u) for u in sublist] for sublist in split_mu_list]

    for i in range(len(num_pkts)):

        W_bar_i = [np.average([item[2] for item in l]) for l in big_split[i]] # Gather W_bar_i
        GG1_priority_theoretical(priority_classes[i], lambda_i[i], 0, mu_i[i], 0, W_bar_i)


    #---------------------------------------------------------------------------------------

    #plt.legend()
    plt.legend(frameon=False)
    plt.show()