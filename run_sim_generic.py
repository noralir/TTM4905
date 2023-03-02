from datetime import datetime
from generic_simulator import generic_simulator, write_input_file, read_input_file


def run_simulator(folder, input_file, runs, data, nth):
    input_variables = read_input_file(folder + input_file)
    folder_nth = folder + "nth/" if nth else nth
    for i in range(runs):
        filename_data = folder + "data/" + str(i) + ".csv" if data else data
        print("start sim", i, "time:", datetime.now().strftime("%H:%M:%S"))
        generic_simulator(input_variables = input_variables, filename_data = filename_data, folder_nth = folder_nth)
        print("  end sim", i, "time:", datetime.now().strftime("%H:%M:%S"))


