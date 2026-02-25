import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# get arrays
file = "./pt2-t4.csv"
df = pd.read_csv(file)
acc = df['yaccelerometer'].to_numpy()
force = df['force'].to_numpy()
time = df['time'].to_numpy()

# line up 
acc = acc + (force[0]-acc[0])

# set up plot
fig = plt.figure()
plt.xlabel("Time [s]")
plt.title("Acceleration and Force over Time")


plt.scatter(time, acc, c="orange", label="Acceleration")
plt.scatter(time, force, label="Force")
plt.legend()



plt.show()
