import matplotlib.pyplot as plt
import numpy as np
import math

from sklearn.linear_model import LinearRegression

# Functions from files
from readcsvfile import readcsvfile


# GATHER DATA
fields, rows = readcsvfile("data/MM1_file_dataset.csv")
delay = [row[2]+row[3] for row in rows]

# HISTORGAM DATA

n, bins, _ = plt.hist(delay, density=False, label="actual distribution", color='aquamarine', bins=13)

x = np.array([(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)])
plt.plot(x, n/n[0])
plt.plot(x, n)

plt.xlabel("delay")
plt.title("title of plot")
plt.legend()
plt.show()


# ---------- MOVING AVERAGE ------------ #
arrival_times1 = np.array([row[1] for row in rows])
inter_arrival_times = np.array([rows[i+1][1] - rows[i][1] for i in range(len(rows)-1)])

data_inputs = len(inter_arrival_times)
part_data_inputs = int(data_inputs * 0.8)
part_of_inter_arrival_times = np.array(inter_arrival_times[:part_data_inputs])
lambda_moving_average = np.average(part_of_inter_arrival_times)
print("PREDICTED INTER ARRIVAL TIME", lambda_moving_average)

f = lambda l, x : l * math.e**(-l * x)
x_moving_average = np.arange(0, 60, 0.25)
y_moving_average = f(1/lambda_moving_average ,x_moving_average)
plt.plot(x_moving_average, y_moving_average)
plt.show()
# ---------------------------------------- #



# ------------- ML ------------------ #
number_packet = np.array([row[0] for row in rows])
time_series = np.array([row[1] for row in rows])
train_number = int(len(time_series) * 0.8)

number_packet_train = number_packet[:train_number].reshape(-1,1)
number_packet_test = number_packet[train_number:].reshape(-1,1)

data_train = time_series[:train_number].reshape(-1,1)
data_test = time_series[train_number:].reshape(-1,1)


regsr=LinearRegression()
regsr.fit(number_packet_train, data_train)

predicted_y= regsr.predict(number_packet_test)
m= regsr.coef_
c= regsr.intercept_
'''
print("Predicted y:\n",predicted_y)
print("slope (m): ",m)
print("y-intercept (c): ",c)
'''

new_y=[ m*i+c for i in np.append(number_packet_train,number_packet_test)]
new_y=np.array(new_y).reshape(-1,1)


plt.scatter(number_packet_train, data_train, color="mediumaquamarine", label="train")
plt.scatter(number_packet_test, data_test, color="palevioletred", label="test")
plt.plot(number_packet, new_y, color="gold", label="predicted line")
plt.xlabel("number")
plt.ylabel("time")
plt.legend()
plt.show()




plt.scatter(number_packet_test, data_test, color="palevioletred", label="test")
plt.scatter(number_packet_test, new_y[train_number:], color="gold", label="predicted line")
plt.xlabel("number")
plt.ylabel("time")
plt.legend()
plt.show()

# ---------------------------------------- #


