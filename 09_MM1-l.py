from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth_sojourn

#run_simulator(folder="09_MM1-l/", input_file="input.json", runs=1000, data=False, nth=True)

#plot_gen(filename_input="09_MM1-l/input.json", filename_data="09_MM1-l/data/0.csv")
plot_gen_nth_sojourn(filename_input="09_MM1-l/input.json", folder_nth="09_MM1-l/nth/", indexes = [0,3])