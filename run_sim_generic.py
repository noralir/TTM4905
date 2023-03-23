from datetime import datetime
import os
from generic_simulator import generic_simulator, write_input_file, read_input_file

'''
folder = "00_MM1/"          # string
input_file = "input.json"   # string
runs = 100                  # int
data = True                 # bool
nth = True                  # bool
'''

def run_simulator(folder, input_file, runs, data, nth):
    # CHECK FOR FOLDERS
    folder_data = folder + "data/"
    if not os.path.exists(folder_data):
        os.makedirs(folder_data)
    folder_nth = folder + "nth/"
    if not os.path.exists(folder_nth):
        os.makedirs(folder_nth)
    # MAKE NEEDED VALUES
    input_variables = read_input_file(folder + input_file)
    folder_nth = folder + "nth/" if nth else nth
    # RUN SIMULATOR
    for i in range(runs):
        filename_data = folder + "data/" + str(i) + ".csv" if data else data
        print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
        generic_simulator(input_variables = input_variables, filename_data = filename_data, folder_nth = folder_nth)
        print("  end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))


