import csv
def readcsvfile(filename):
       fields, rows = [], []
       with open(filename, 'r') as file:
              csvreader = csv.reader(file)
              fields = next(csvreader)
              rows = [[int(row[0]), float(row[1]), float(row[2]), float(row[3])] for row in csvreader]
       return fields, rows