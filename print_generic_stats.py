import json
import numpy as np
from readdatacsv import read_data_csv

def generic_stats(filename_input, filename_data):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    fields_data, rows_data = read_data_csv(filename_data)

    wait = [row[2] for row in rows_data]
    processing = [row[3] for row in rows_data]
    delay = [row[2]+row[3] for row in rows_data]


    mean_delay = np.mean(delay)

    print(mean_delay)