from datetime import datetime
from generic_simulator import generic_simulator, write_input_file, read_input_file

MM1_input = read_input_file("01_MM1/MM1_input.json")
for i in range(100):
    print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
    generic_simulator(
        input_variables = read_input_file("03_MM1/MM1_input.json"), 
        filename_data = "03_MM1/data/" + str(i) + ".csv", 
        folder_nth="03_MM1/nth/"
    )
    print("end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))