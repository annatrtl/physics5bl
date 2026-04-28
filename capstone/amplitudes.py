import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd

# data
freq = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]) #kHz

file1 = './amplitudes-04-22-first.csv' #300 n
file2 = './amplitudes-04-22-second.csv' #140 n
file3 = './amplitudes-04-22-third.csv' #93 n

df1 = pd.read_csv(file1)
dB1 = df1['dB'].to_numpy() #dB
time1 = df1['time'].to_numpy() #s

df2 = pd.read_csv(file2)
dB2 = df2['dB'].to_numpy() #dB
time2 = df2['time'].to_numpy() #s

df3 = pd.read_csv(file3)
dB3 = df3['dB'].to_numpy() #dB
time3 = df3['time'].to_numpy() #s

# calc
time2 = time2 - time2[0] #s
time3 = time3 - time3[0] #s

# raw data plot setup
fig = plt.figure()
plt.title('')
plt.xlabel('time')
plt.ylabel('kHz')
plt.scatter(time1, dB1, color="red", label="300n", marker="o")
plt.scatter(time2, dB2, color="blue", label="140n", marker="o")
plt.scatter(time3, dB3, color="green", label="93n", marker="o")

plt.legend()

# average data calc
dB1_avg = np.array([np.mean(dB1[0:60]), np.mean(dB1[61:112]), np.mean(dB1[113:202]), np.mean(dB1[203:227]), np.mean(dB1[229:283]), np.mean(dB1[284:338]), np.mean(dB1[339:395]), np.mean(dB1[396:451]), np.mean(dB1[452:503]), np.mean(dB1[504:558]), np.mean(dB1[559:612]), np.mean(dB1[613:664]), np.mean(dB1[665:716]), np.mean(dB1[717:767]), np.mean(dB1[768:821]), np.mean(dB1[822:875]), np.mean(dB1[876:929]), np.mean(dB1[930:983]), np.mean(dB1[984:1032])])
dB2_avg = np.array(np.mean(dB1[0:0]), )

# average data plot setup
fig = plt.figure()
plt.title('')
plt.xlabel('')
plt.ylabel('')
plt.scatter(freq, dB1_avg)


plt.legend()
plt.show()
