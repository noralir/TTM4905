from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats

# create input file
input_variables = {
    "avg_pkt_ia_time": [[15*100]*100], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [["M"]*100], 

    "avg_pkt_len_bits": [[100]*100], 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [["M"]*100], 

    "capacity": 1, 
    "num_pkts": [[100]*100],
    "num_sources" : [[1]*100]
}

folder = "19_MM1-100s/"

#write_input_file(input_variables, folder+"input.json")

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")

#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")