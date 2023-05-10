from run_sim_generic import *
from plot_generic import *
from print_generic_stats import generic_stats

folder = "30_MM1/"

input_variables = {
    "avg_pkt_ia_time": [15], 
    "dist_type_pkt_ia_time": ["M"], 

    "avg_pkt_len_bits": [10], 
    "variance_pkt_len_bits": [0], 
    "sigma_squared_pkt_len": [0],
    "dist_type_pkt_len": ["M"], 

    "capacity": 1, 
    "num_pkts": [100000]
}

if not os.path.exists(folder):
    os.makedirs(folder)

write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_pdf")

