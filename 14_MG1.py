from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth
from print_generic_stats import generic_stats

folder = "14_MG1/"

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

#plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")

generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")