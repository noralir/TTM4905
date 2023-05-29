from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats
from create_list_with_given_average import create_list_with_given_average

folder = os.path.basename(__file__).split('.')[0] + "/"
n = int(folder[7:-2])


avg_pkt_ia_time1 = create_list_with_given_average(n=n, avg=15,type="lambda")
type_pkt_ia1 = "D"

avg_pkt_len_bits = [10]*n
type_pkt_len = "D"


input_variables = {
    "avg_pkt_ia_time": [avg_pkt_ia_time1], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [[type_pkt_ia1]*n], 

    "avg_pkt_len_bits": [avg_pkt_len_bits], 
    "dist_type_pkt_len": [[type_pkt_len]*n], 

    "capacity": 1, 
    "num_pkts": [[10000]*n],
    "num_sources": [[1]*n]
}                                                                                                                               

if not os.path.exists(folder):
    os.makedirs(folder)

write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)


plot_multiple_sources_no_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf", color_choice="two_pink")
