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
plt.title('Decibel value as frequency is changed over time')
plt.xlabel('Time, adjusted to zero for each coil [s]')
plt.ylabel('Decibels value [dB]')
plt.scatter(time1, dB1, color="red", label="300n", marker="o")
plt.scatter(time2, dB2, color="blue", label="140n", marker="o")
plt.scatter(time3, dB3, color="green", label="93n", marker="o")

plt.legend()

# average data calc
dB1_avg = np.array([np.mean(dB1[0:60]), np.mean(dB1[61:112]), np.mean(dB1[113:202]), np.mean(dB1[203:227]), np.mean(dB1[229:283]), np.mean(dB1[284:338]), np.mean(dB1[339:395]), np.mean(dB1[396:451]), np.mean(dB1[452:503]), np.mean(dB1[504:558]), np.mean(dB1[559:612]), np.mean(dB1[613:664]), np.mean(dB1[665:716]), np.mean(dB1[717:767]), np.mean(dB1[768:821]), np.mean(dB1[822:875]), np.mean(dB1[876:929]), np.mean(dB1[930:983]), np.mean(dB1[984:1032])])
dB2_avg = np.array([np.mean(dB2[0:94]), np.mean(dB2[95:159]), np.mean(dB2[161:233]), np.mean(dB2[234:307]), np.mean(dB2[308:383]), np.mean(dB2[385:456]), np.mean(dB2[458:529]), np.mean(dB2[531:605]), np.mean(dB2[607:682]), np.mean(dB2[684:762]), np.mean(dB2[763:832]), np.mean(dB2[833:903]), np.mean(dB2[904:976]), np.mean(dB2[977:1041]), np.mean(dB2[1042:1072]), np.mean(dB2[1073:1198]), np.mean(dB2[1200:1273]), np.mean(dB2[1274:1347]), np.mean(dB2[1349:1429])])
dB3_avg = np.array([np.mean(dB3[0:74]), np.mean(dB3[76:149]), np.mean(dB3[152:219]), np.mean(dB3[220:292]), np.mean(dB3[293:365]), np.mean(dB3[366:441]), np.mean(dB3[442:512]), np.mean(dB3[514:589]), np.mean(dB3[590:665]), np.mean(dB3[667:739]), np.mean(dB3[741:807]), np.mean(dB3[808:887]), np.mean(dB3[889:960]), np.mean(dB3[961:1002]), np.mean(dB3[1003:1044]), np.mean(dB3[1045:1086]), np.mean(dB3[1087:1128]), np.mean(dB3[1129:1169]), np.mean(dB3[1129:1169])])


# average data plots setup
fig = plt.figure()
plt.title('Decibel value at each frequency for 300n solenoid')
plt.xlabel('Frequency [kHz]')
plt.ylabel('Decibel average at each frequency [dB]')
plt.scatter(freq, dB1_avg, color="red", label="300n")

plt.legend()


fig = plt.figure()
plt.title('Decibel value at each frequency for 140n solenoid')
plt.xlabel('Frequency [kHz]')
plt.ylabel('Decibel average at each frequency [dB]')
plt.scatter(freq, dB2_avg, color="blue", label="140n")

plt.legend()


fig = plt.figure()
plt.title('Decibel value at each frequency for 93n solenoid')
plt.xlabel('Frequency [kHz]')
plt.ylabel('Decibel average at each frequency [dB]')
plt.scatter(freq, dB3_avg, color="green", label="93n")

plt.legend()

# delta dB
delta_dB_93to140 = np.mean((dB2_avg[:-2] - dB3_avg[:-2]))
delta_dB_140to300 = np.mean((dB1_avg - dB2_avg))
delta_dB_93to300 = np.mean((dB1_avg[:-2] - dB3_avg[:-2]))
print(dB3_avg - dB1_avg)

print(f"Experimental (140n - 93n) dB: {delta_dB_93to140}")
print(f"Theoretical (140n - 93n) dB: {20*np.log(93/140)}")


print(f"Experimental (300n - 140n) dB: {delta_dB_140to300}")
print(f"Theoretical (300n - 140n) dB: {20*np.log(140/300)}")


print(f"Experimental (300n - 93n) dB: {delta_dB_93to300}")
print(f"Theoretical (300n - 93n) dB: {20*np.log(93/300)}")

plt.show()
