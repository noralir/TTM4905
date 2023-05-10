from run_sim_generic import run_simulator
from plot_generic import plot_gen_file, plot_gen_nth

folder = "09_MM1-l/"

#run_simulator(folder="09_MM1-l/", input_file="input.json", runs=1, data=True, nth=False)
'''
plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_cdf")
plot_gen_file(filename_input=folder+"input.json", filename_data=folder+"data/0.csv", plot_type="wait_pdf")
plot_gen_file(filename_input=folder+"/input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_pdf")
plot_gen_file(filename_input=folder+"/input.json", filename_data=folder+"data/0.csv", plot_type="sojourn_cdf")
'''
plot_gen_nth(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes = [0,1,2,3,4], plot_type="wait_pdf")

'''
plot_gen_nth(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes = [0,1], plot_type="wait_cdf")
plot_gen_nth(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes = [0,1], plot_type="sojourn_cdf")
plot_gen_nth(filename_input=folder+"input.json", folder_nth=folder+"nth/", indexes = [0,1], plot_type="sojourn_pdf")
'''