from run_sim_generic import run_simulator
from plot_generic import plot_priority_file, MG1_priority_theoretical
from print_generic_stats import generic_stats

folder = "17_GG1-pri/"

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_priority_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", dist_type="GG")

#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")