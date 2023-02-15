import simpy
import csv
import json
import numpy as np
import os

def inter_arrival_time(dist_type_pkt_ia_time, avg_pkt_ia_time_us):
    if dist_type_pkt_ia_time == 'M':
        return np.random.exponential(avg_pkt_ia_time_us)
    elif dist_type_pkt_ia_time == 'D':
        return avg_pkt_ia_time_us
    else:
        return avg_pkt_ia_time_us # D is standard

def packet_size(dist_type_pkt_len, avg_pkt_len_bits):
    if dist_type_pkt_len == 'M':
        return int(np.random.exponential(avg_pkt_len_bits))
    elif dist_type_pkt_len == 'D':
        return avg_pkt_len_bits
    else:
        return avg_pkt_len_bits

def generic_simulator(input_variables, filename_data, folder_nth):

    def packetgenerator(env):
        for i in range(len(input_variables["num_pkts"])):
            j = 0 
            while j <= input_variables["num_pkts"][i]:
                yield env.timeout(inter_arrival_time(input_variables["dist_type_pkt_ia_time"][i], input_variables["avg_pkt_ia_time_us"][i]))
                env.process(packet(env, packet_size(input_variables["dist_type_pkt_len"][i], input_variables["avg_pkt_len_bits"][i]), j, i))
                j += 1
            j = 0

    def packet(env, pkt_size_bits, number, dist_i):
        t_generated_us = env.now
        n_in_queue = len(buffer.queue)
        with buffer.request() as req:
            yield req
            t_processing_start = env.now
            yield env.timeout(pkt_size_bits / input_variables["capacity_bps"] * 10**6)
            t_processing_end = env.now 
        # Calculate data
        t_buffer_us = t_processing_start - t_generated_us
        t_processing_us = t_processing_end - t_processing_start
        # Save data 
        if filename_data != False:
            writer.writerow([number, t_generated_us, t_buffer_us, t_processing_us, pkt_size_bits, n_in_queue])
        if number in [0, 10, 100, 1000, 10000, 100000, 1000000] and folder_nth != False:
            filename = folder_nth + str(dist_i) + '/' + str(number) +'.csv'
            exist = os.path.isfile(filename)
            with open(filename, 'a', newline='') as fileN:
                writerN = csv.writer(fileN)
                if not exist:
                    writerN.writerow(["number", "t_generated_us", "t_buffer_us", "t_processing_us", "pkt_size_bits", "n_in_queue"])
                writerN.writerow([number, t_generated_us, t_buffer_us, t_processing_us, pkt_size_bits, n_in_queue])

    if filename_data != False:
        f_data = open(filename_data, 'w', newline='')
        writer = csv.writer(f_data)
        writer.writerow(["number", "t_generated_us", "t_buffer_us", "t_processing_us", "pkt_size_bits", "n_in_queue"])

    env = simpy.Environment()
    buffer = simpy.Resource(env)
    env.process(packetgenerator(env))
    env.run()
    if filename_data != False:
        f_data.close()


def write_input_file(input_variables, filename_input):
    with open(filename_input, 'w') as f_input:
        json.dump(input_variables, f_input)

def read_input_file(filename_input):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    return input_variables

