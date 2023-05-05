from run_sim_generic import *
from plot_generic import plot_priority_file, MG1_priority_theoretical
from print_generic_stats import generic_stats

folder = "15_MG1-pri/"

input_variables = {
    "avg_pkt_ia_time": [[23]*3], 
    "dist_type_pkt_ia_time": [["M", "M", "M"]], 

    "avg_pkt_len_bits": [[10,5,7]], 
    "variance_pkt_len_bits": [[0,5,0]], 
    "sigma_squared_pkt_len": [[0,8.333,49]],
    "dist_type_pkt_len": [["D", "G_uniform", "M"]], 

    "capacity": 1, 
    "num_pkts": [[1000000, 1000000, 1000000]],
    "num_sources" : [[1,2,3]]
}
write_input_file(input_variables, folder+"input.json")

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_priority_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")

