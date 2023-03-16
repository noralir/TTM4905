from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth_sojourn

folder="12_MD1-l/"

#run_simulator(folder = folder, input_file = "input.json", runs = 500, data = False, nth = True)

plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_cdf")
plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")
plot_gen_nth_sojourn(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes=[0,1], plot_type="wait_cdf")
plot_gen_nth_sojourn(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes=[0,1], plot_type="sojourn_pdf")