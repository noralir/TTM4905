import simpy
import csv
import json
import numpy as np
import os

check_list = []

def inter_arrival_time(dist_type_pkt_ia_time, avg_pkt_ia_time):
    if dist_type_pkt_ia_time == 'M':
        return np.random.exponential(avg_pkt_ia_time)
    elif dist_type_pkt_ia_time == 'D':
        return avg_pkt_ia_time
    elif dist_type_pkt_ia_time == 'G_uniform':
        return np.random.uniform(0, avg_pkt_ia_time*2)
    return avg_pkt_ia_time # D is standard

def packet_size(dist_type_pkt_len, avg_pkt_len_bits):
    if dist_type_pkt_len == 'M':
        return np.random.exponential(avg_pkt_len_bits)
    elif dist_type_pkt_len == 'D':
        return avg_pkt_len_bits
    elif dist_type_pkt_len == 'G_uniform':
        return np.random.uniform(0, avg_pkt_len_bits*2)
    return avg_pkt_len_bits

def generic_simulator(input_variables, filename_data = False, folder_nth = False, multiple_classes = False):

    def packetgenerator(env):
        global check_list
        if "num_sources" in input_variables:

            for k in range(len(input_variables["num_pkts"])): # index k in input-file
                '''
                EXAMPLES
                num_sources_k = [1,2,3] # Class/priority
                num_pkts_k = [100, 100, 100]
                '''
                # If there is a list at index k, keep it, if not change to a list with priority getting lower, e.g. 3 turns into [0,1,2]
                num_sources_k = input_variables["num_sources"][k] if type(input_variables["num_sources"][k]) == type([]) else [i for i in range(input_variables["num_sources"][k])]
                num_pkts_k = input_variables["num_pkts"][k] if type(input_variables["num_pkts"][k]) == type([]) else [input_variables["num_pkts"][k]/len(num_sources_k) for i in range(len(num_sources_k))]
                # Start subgenerators
                for i in range(len(num_sources_k)):
                    env.process(sub_packetgenerator(env=env, priority=num_sources_k[i], num_pkts=num_pkts_k[i], index=k, subindex=i))
                # Don't start next round before all are finished
                while len(check_list) < len(num_sources_k): 
                    yield env.timeout(1)
                check_list = []
        else: # Only one class, no priority
            for i in range(len(input_variables["num_pkts"])):
                j = 0 
                while j <= input_variables["num_pkts"][i]:
                    yield env.timeout(inter_arrival_time(dist_type_pkt_ia_time = input_variables["dist_type_pkt_ia_time"][i], 
                                                         avg_pkt_ia_time = input_variables["avg_pkt_ia_time"][i]))
                    env.process(packet(env = env, 
                                       pkt_size_bits = packet_size(dist_type_pkt_len = input_variables["dist_type_pkt_len"][i], 
                                                                   avg_pkt_len_bits = input_variables["avg_pkt_len_bits"][i]), 
                                       number = str(j)+"00", # add trailing 0s to be able to be handeled by mulitple classes 
                                       dist_i = i))
                    j += 1
                j = 0
    
    def sub_packetgenerator(env, priority, num_pkts, index, subindex):
        j = 0
        while j <= num_pkts:
            yield env.timeout(inter_arrival_time(dist_type_pkt_ia_time=input_variables["dist_type_pkt_ia_time"][index] if type(input_variables["dist_type_pkt_ia_time"][index]) == type("M") else input_variables["dist_type_pkt_ia_time"][index][subindex], 
                                                 avg_pkt_ia_time=input_variables["avg_pkt_ia_time"][index] if type(input_variables["avg_pkt_ia_time"][index]) == type(1) else input_variables["avg_pkt_ia_time"][index][subindex]))
            env.process(packet(env=env, 
                               pkt_size_bits=packet_size(dist_type_pkt_len = input_variables["dist_type_pkt_len"][index][subindex] if type(input_variables["dist_type_pkt_len"][index]) == type([]) else input_variables["dist_type_pkt_len"][index], 
                                                         avg_pkt_len_bits = input_variables["avg_pkt_len_bits"][index][subindex] if type(input_variables["avg_pkt_len_bits"][index]) == type([]) else input_variables["avg_pkt_len_bits"][index]), 
                               number=str(j)+str(subindex)+str(priority), 
                               dist_i=index, 
                               priority = priority))
            j += 1
        check_list.append(priority)


    def packet(env, pkt_size_bits, number, dist_i, priority = 0):
        t_generated = env.now
        n_in_queue = len(buffer.queue)
        with buffer.request(priority=priority) as req:
            yield req
            t_processing_start = env.now
            yield env.timeout(pkt_size_bits / input_variables["capacity"])
            t_processing_end = env.now 
        # Calculate data
        t_buffer = t_processing_start - t_generated
        t_processing = t_processing_end - t_processing_start
        # Save data 
        if filename_data:
            writer.writerow([number, t_generated, t_buffer, t_processing, pkt_size_bits, n_in_queue])
        number_int = int(number[:-2])    
        if number_int in [0, 10, 100, 1000, 10000, 100000, 1000000] and folder_nth:
            folder_path = folder_nth + str(dist_i)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = folder_nth + str(dist_i) + '/' + str(number) +'.csv'
            exist = os.path.isfile(filename)
            with open(filename, 'a', newline='') as fileN:
                writerN = csv.writer(fileN)
                if not exist:
                    writerN.writerow(["number", "t_generated", "t_buffer", "t_processing", "pkt_size_bits", "n_in_queue"])
                writerN.writerow([number, t_generated, t_buffer, t_processing, pkt_size_bits, n_in_queue])

    if filename_data:
        f_data = open(filename_data, 'w', newline='')
        writer = csv.writer(f_data)
        writer.writerow(["number", "t_generated", "t_buffer", "t_processing", "pkt_size_bits", "n_in_queue"])

    env = simpy.Environment()
    buffer = simpy.PriorityResource(env)
    env.process(packetgenerator(env))
    env.run()
    if filename_data:
        f_data.close()


def write_input_file(input_variables, filename_input):
    with open(filename_input, 'w') as f_input:
        json.dump(input_variables, f_input)

def read_input_file(filename_input):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    return input_variables

