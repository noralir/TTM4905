import csv
import numpy as np
def read_data_csv(filename):
       fields, rows = [], []
       with open(filename, 'r') as file:
              csvreader = csv.reader(file)
              fields = next(csvreader)
              rows = np.array([np.array([
                     int(row[0]), 
                     float(row[1]), 
                     float(row[2]), 
                     float(row[3]), 
                     float(row[4]), 
                     int(row[5])
              ]) for row in csvreader])
       return fields, rows