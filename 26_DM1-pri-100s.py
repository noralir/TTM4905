from generic_simulator import write_input_file
from run_sim_generic import run_simulator
from plot_generic import *
from print_generic_stats import generic_stats
from create_list_with_given_average import create_list_with_given_average

n = 100
folder = "26_DM1-pri-100s/"



avg_pkt_ia_time1 = create_list_with_given_average(n=n, avg=120,type="lambda")
avg_pkt_ia_time2 = create_list_with_given_average(n=n, avg=180,type="lambda")
avg_pkt_ia_time3 = create_list_with_given_average(n=n, avg=150,type="lambda")
type_pkt_ia = "D"


avg_pkt_len_bits = create_list_with_given_average(n=n, avg=17.5,type="mu")
type_pkt_len = "M"


input_variables = {
    "avg_pkt_ia_time": [[*avg_pkt_ia_time1, *avg_pkt_ia_time2, *avg_pkt_ia_time3]], 
    "sigma_squared_pkt_ia_time":[],
    "dist_type_pkt_ia_time": [[*[type_pkt_ia]*n, *[type_pkt_ia]*n, *[type_pkt_ia]*n]], 

    "avg_pkt_len_bits": [[*avg_pkt_len_bits, *avg_pkt_len_bits, *avg_pkt_len_bits]], 
    "sigma_squared_pkt_len": [],
    "dist_type_pkt_len": [[*[type_pkt_len]*n, *[type_pkt_len]*n, *[type_pkt_len]*n]], 

    "capacity": 1, 
    "num_pkts": [[*[1000]*n ,*[1000]*n ,*[1000]*n]],
    "num_sources" : [[*[1]*n ,*[2]*n ,*[3]*n]]
}                                                                                                                               


if not os.path.exists(folder):
    os.makedirs(folder)



#write_input_file(input_variables, folder+"input.json")
#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_multiple_sources_with_priority(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_pdf")
