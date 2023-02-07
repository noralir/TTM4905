import simpy
import csv
import json
import numpy as np
import os

def generic_simulator(input_variables, filename_data, folder_nth):
    
    def packetgenerator(env):
        i = 0
        while i <= input_variables["num_pkts"]:
            if input_variables["dist_type_pkt_ia_time"] == 'M':
                yield env.timeout(np.random.exponential(input_variables["avg_pkt_ia_time_us"])) 
            elif input_variables["dist_type_pkt_ia_time"] == 'D':
                yield env.timeout(input_variables["avg_pkt_ia_time_us"])
            else:
                yield env.timeout(input_variables["avg_pkt_ia_time_us"]) # D is standard
            env.process(packet(env, i))
            i += 1

    def packet(env, number):
        t_generated_us = env.now
        n_in_queue = len(buffer.queue)
        pkt_size_bits = input_variables["avg_pkt_len_bits"]
        if input_variables["dist_type_pkt_len"] == 'M':
            pkt_size_bits = int(np.random.exponential(input_variables["avg_pkt_len_bits"]))
        elif input_variables["dist_type_pkt_len"] == 'M':
            pkt_size_bits = input_variables["avg_pkt_len_bits"]
        with buffer.request() as req:
            yield req
            t_processing_start = env.now
            yield env.timeout(pkt_size_bits / input_variables["capacity_bps"] * 10**6)
            t_processing_end = env.now 
        # Calculate data
        t_buffer_us = t_processing_start - t_generated_us
        t_processing_us = t_processing_end - t_processing_start
        # Save data 
        writer.writerow([number, t_generated_us, t_buffer_us, t_processing_us, pkt_size_bits, n_in_queue])
        if number in [0, 10, 100, 1000, 10000, 100000, 1000000]:
            filename = folder_nth + str(number) +'.csv'
            exist = os.path.isfile(filename)
            with open(filename, 'a', newline='') as fileN:
                writerN = csv.writer(fileN)
                if not exist:
                    writerN.writerow(["number", "t_generated_us", "t_buffer_us", "t_processing_us", "pkt_size_bits", "n_in_queue"])
                writerN.writerow([number, t_generated_us, t_buffer_us, t_processing_us, pkt_size_bits, n_in_queue])

    f_data = open(filename_data, 'w', newline='')
    writer = csv.writer(f_data)
    writer.writerow(["number", "t_generated_us", "t_buffer_us", "t_processing_us", "pkt_size_bits", "n_in_queue"])

    env = simpy.Environment()
    buffer = simpy.Resource(env)
    env.process(packetgenerator(env))
    env.run()
    f_data.close()


def write_input_file(input_variables, filename_input):
    with open(filename_input, 'w') as f_input:
        json.dump(input_variables, f_input)

def read_input_file(filename_input):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)
    return input_variables

