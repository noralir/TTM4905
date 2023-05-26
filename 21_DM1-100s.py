from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats
from create_list_with_given_average import create_list_with_given_average

avg_pkt_ia_time = create_list_with_given_average(n=100, avg=15)

input_variables = {
    "avg_pkt_ia_time": [avg_pkt_ia_time], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [["D"]*100], 

    "avg_pkt_len_bits": [[10]*100], 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [["M"]*100], 

    "capacity": 1, 
    "num_pkts": [[1000]*100],
    "num_sources" : [[1]*100]
}                                                                                                                               

folder = "21_DM1-100s/"
if not os.path.exists(folder):
    os.makedirs(folder)

#write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)
plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf", color_choice="two_orange")
#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")

#folder2 = "20_DM1-10s/"
#plot_multiple_sources_no_priority(filename_input=folder2+"input.json", filename_data=folder2+"data/0.csv", plot_type="sojourn_pdf")