from datetime import datetime
from generic_simulator import generic_simulator, write_input_file, read_input_file

MM1_input = read_input_file("01_MM1/MM1_input.json")
for i in range(10):
    print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
    generic_simulator(
        input_variables=MM1_input,
        filename_data='01_MM1/MM1_data/MM1_' + str(i) + '_data.csv')
    print("end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))