from run_sim_generic import run_simulator
from plot_generic import plot_MG1_priority_file
from print_generic_stats import generic_stats

folder = "15_MG1-pri/"

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_MG1_priority_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")

#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")