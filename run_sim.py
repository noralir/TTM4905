from datetime import datetime
from generic_simulator import generic_simulator, write_input_file, read_input_file

folder = "06_MM1/"

for i in range(1):
    print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
    generic_simulator(
        input_variables = read_input_file(folder + "input.json"), 
        filename_data = folder + "data/" + str(i) + ".csv", 
        #filename_data = False,
        #folder_nth = folder + "nth/"
        folder_nth = False
    )
    print("  end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))