from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth, plot_gen_nth_single_plots

folder = "11_MM1-l-u/"

#run_simulator(folder = "11_MM1-l-u/", input_file = "input.json", runs = 3000, data = False, nth = True)

#plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_cdf")
#plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")
#plot_gen_nth(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes=[0,1,2,3,4], plot_type="wait_pdf")

plot_gen_nth_single_plots(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes=[0,1,2,3,4], plot_type="wait_pdf")
