from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats

# create input file
input_variables = {
    "avg_pkt_ia_time": [[15*10]*10], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [["M"]*10], 

    "avg_pkt_len_bits": [[10]*10], 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [["M"]*10], 

    "capacity": 1, 
    "num_pkts": [[10000]*10],
    "num_sources" : [[1]*10]
}                                                                                                                               

folder = "18_MM1-10s/"

#write_input_file(input_variables, folder+"input.json")

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")

#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")