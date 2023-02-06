import simpy
import numpy as np
import csv
import matplotlib.pyplot as plt
import math

from read_data_csv import read_data_csv

SIM_TIME = 10000 #µs
lambda_arrival = 1/20 #1/µs || packet generated every 20 µs
pkt_size = 1/8000 #1/bits || packet size (1/1000 1/bytes)

# Gathering values
packets = 0
waiting_time = 0
processing_time = 0
sojourn_time = 0

# File
f = open('MD1_file.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(["number", "t_generated", "t_buffer", "t_processing"])

def packetgenerator(env):
    i = 0
    while True:
        yield env.timeout(np.random.exponential(1/lambda_arrival)) 
        env.process(packet(env, i))
        i += 1

def packet(env, number):
    global packets, waiting_time, processing_time, sojourn_time
    t_generated = env.now
    size = 1/pkt_size

    with buffer.request() as req:
        yield req
        t_processing_start = env.now
        yield env.timeout(size / buffer_capacity * 10**6)
        t_processing_end = env.now 

    # Calculate data
    t_buffer = t_processing_start - t_generated
    t_processing = t_processing_end - t_processing_start

    # Save data
    packets += 1
    waiting_time += t_buffer
    processing_time += t_processing
    sojourn_time += t_buffer + t_processing

    # Printing
    writer.writerow([number, t_generated, t_buffer, t_processing])
    #print(f"{number}\t{t_generated}\t{t_processing}\t{t_buffer}")

env = simpy.Environment()

# BUFFER
buffer_capacity = 1*10**9 #bps (1 Gbps)
buffer = simpy.Resource(env)

# RUN
env.process(packetgenerator(env))
env.run(until=SIM_TIME)

# Close file
f.close()

# --- OBSERVED VALUES ----------------------- #
O_S = sojourn_time/packets
O_W = waiting_time/packets
# ------------------------------------------- #

# ---- THEORETICAL VALUES ------------------- #
l = lambda_arrival
m = 1/((1/pkt_size)/buffer_capacity*10**6)
rho = l/m

#E_Q = rho**2/(1-rho) # expected queue length
E_S = 1/m + rho/(2*m*(1-rho)) # expected sojourn time
E_W = rho/(2*m*(1-rho)) # expected waiting time
# ------------------------------------------ #

# ---- PRINTING ---------------------------- #
print(f"theoretical sojourn time: {E_S} \nobserved sojourn time: {O_S}")
print(f"theoretical waiting time: {E_W} \nobserved waiting time: {O_W}")
# ------------------------------------------ #

# ---------------------- PLOT --------------- #
fields, rows = read_data_csv("MM1_file.csv")
delay = [row[2]+row[3] for row in rows]
n, bins, _ = plt.hist(delay, density=True, label="actual distribution", color='aquamarine', bins=50)

f = lambda l, x : l * math.e**(-l * x) + pkt_size

plt.plot(np.arange(0, 100, 0.25), f(l, np.arange(0, 100, 0.25)), label="theoretical value", color="blueviolet")
plt.xlabel("sojourn time")
plt.title("title of plot")
plt.legend()
plt.show()

# ------------------------------------------ #
