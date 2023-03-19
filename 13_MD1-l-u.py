from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth

folder="13_MD1-l-u/"

run_simulator(folder = folder, input_file = "input.json", runs = 1000, data = False, nth = True)

#plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv")
#plot_gen_nth_sojourn(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes=[0,1])