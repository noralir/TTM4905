import os
import csv
from readdatacsv import read_data_csv

def nth_packet(packet_n, folder_data, targetfile):
    f_data = open(targetfile, 'w', newline='')
    writer = csv.writer(f_data)
    writer.writerow(["number", "t_generated_us", "t_buffer_us", "t_processing_us", "pkt_size_bits"])
    for file in os.listdir(folder_data):
        f = os.path.join(folder_data, file)
        if os.path.isfile(f):
            fields, rows = read_data_csv(f)
            writer.writerow(rows[packet_n])
    f_data.close()

#nth_packet(packet_n=10000, folder_data="01_MM1/MM1_data", targetfile="01_MM1/nth_packet/10000.csv")