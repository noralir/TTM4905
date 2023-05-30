import json
import numpy as np
from readdatacsv import read_data_csv

def generic_stats(filename_input, filename_data, dist_type="MG"):
    with open(filename_input, 'r') as f_input:
        input_variables = json.load(f_input)

    fields_data, rows_data = read_data_csv(filename_data)

    wait = [row[2] for row in rows_data]
    processing = [row[3] for row in rows_data]
    delay = [row[2]+row[3] for row in rows_data]

    if dist_type == "MG":
        avg_pkt_ia_time = input_variables["avg_pkt_ia_time"][0]
        avg_pkt_len_bits = input_variables["avg_pkt_len_bits"][0]
        variance_pkt_len_bits = input_variables["variance_pkt_len_bits"][0]

        l = 1/avg_pkt_ia_time
        u = 1/avg_pkt_len_bits
        s = variance_pkt_len_bits
        r = l/u
        theoretical_expected_delay = (r**2 + l**2*s)/(2*l*(1-r))
        print("Theoretical expected wait time:", theoretical_expected_delay)


    mean_delay = np.mean(delay)
    print("Mean wait:", np.mean(wait))
    print("Mean delay:",mean_delay)