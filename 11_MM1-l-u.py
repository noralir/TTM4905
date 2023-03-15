from run_sim_generic import run_simulator
from plot_generic import plot_gen, plot_gen_nth

run_simulator(folder = "11_MM1-l-u/", input_file = "input.json", runs = 100, data = False, nth = True)

#plot_gen(filename_input="11_MM1-l-u/input.json", filename_data="11_MM1-l-u/data/0.csv")
#plot_gen_nth(filename_input="11_MM1-l-u/input.json", folder_nth="11_MM1-l-u/nth/", indexes=[0,1])
