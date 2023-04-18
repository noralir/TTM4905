from run_sim_generic import run_simulator
from plot_generic import plot_MG1_priority_file, MG1_priority_theoretical, plot_gen_file, plot_wait_times
from print_generic_stats import generic_stats

folder = "16_GG1/"

#run_simulator(folder=folder, input_file="input.json", runs=1, data=True, nth=False)

plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_pdf")
plot_wait_times(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")

#plot_MG1_priority_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")
#generic_stats(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")