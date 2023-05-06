from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats
from create_list_with_given_average import create_list_with_given_average

n = 1000
folder = "24_DD1-1000s/"



avg_pkt_ia_time = create_list_with_given_average(n=n, avg=20)


avg_pkt_len_bits = [[x/10 for x in list(range(80,180))]*10]
avg_pkt_len_bits = [[14]*n]

input_variables = {
    "avg_pkt_ia_time": [avg_pkt_ia_time], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [["D"]*n], 

    "avg_pkt_len_bits": avg_pkt_len_bits, 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [["D"]*n], 

    "capacity": 1, 
    "num_pkts": [[1000]*n],
    "num_sources" : [[1]*n]
}                                                                                                                               


if not os.path.exists(folder):
    os.makedirs(folder)

#write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)
#plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_cdf", dist_type="MD")
plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_pdf", dist_type="MD")
#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")

'''
folder2="07_MD1/"
plot_gen_file(filename_input=folder2+"input.json", filename_data=folder2+"data/0.csv", plot_type="wait_pdf")
plot_gen_file(filename_input=folder2+"input.json", filename_data=folder2+"data/0.csv", plot_type="wait_cdf")
'''