from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats
from create_list_with_given_average import create_list_with_given_average

n = 100
folder = "23_DD1-100s/"



avg_pkt_ia_time = create_list_with_given_average(n=n, avg=15)


avg_pkt_len_bits = [[x/10 for x in list(range(80,180))]]


input_variables = {
    "avg_pkt_ia_time": [avg_pkt_ia_time], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [["D"]*n], 

    "avg_pkt_len_bits": avg_pkt_len_bits, 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [["D"]*n], 

    "capacity": 1, 
    "num_pkts": [[100]*n],
    "num_sources" : [[1]*n]
}                                                                                                                               


if not os.path.exists(folder):
    os.makedirs(folder)

#write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)
plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")
#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")