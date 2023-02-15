from datetime import datetime
from generic_simulator import generic_simulator, write_input_file, read_input_file

folder = "05_MM1-MD1/"

for i in range(10000):
    print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
    generic_simulator(
        input_variables = read_input_file(folder + "input.json"), 
        #filename_data = folder + "data/" + str(i) + ".csv", 
        filename_data = False,
        folder_nth = folder + "nth/"
    )
    print("  end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))