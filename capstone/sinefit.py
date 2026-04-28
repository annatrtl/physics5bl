import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# data
#file = './TEK00000.csv' #noise data
#file = './TEK00001.csv' #test1 data
#file = './TEK00002.csv' #test2 data
file1 = './300hz-140n.csv' 
file2 = './300hz-300n.csv' 
file3 = './300hz-93n.csv' 
#file = './sweep300to900hz-93n.csv' 
ang_freq = 2*np.pi*300

df1 = pd.read_csv(file1)
v1 = df1['CH1'].to_numpy() #V
time1 = df1['TIME'].to_numpy() #s

df2 = pd.read_csv(file2)
v2 = df2['CH1'].to_numpy() #V
time2 = df2['TIME'].to_numpy() #s

df3 = pd.read_csv(file3)
v3 = df3['CH1'].to_numpy() #V
time3 = df3['TIME'].to_numpy() #s

# sine function
def sin(t, a, w, phi):
    return a*np.sin(w*t - phi)

# 140n plot
fig = plt.figure()
plt.title('Detected sound fit to sine wave for 140n solenoid')
plt.ylabel('Voltage [V]')
plt.xlabel('Time [s]')
plt.scatter(time1, v1, color="blue", label="140n oscilloscope data")

guesses1 = [0.003, ang_freq, 0.05]
popt1, pcov1 = curve_fit(sin, time1, v1, p0=guesses1) 
plt.plot(time1, sin(time1, *popt1), 'r-', color="orange", label=f"{popt1[0]:.9f}*sin({popt1[1]:.9f}t + {popt1[2]:.9f}")

plt.legend()


# 300n plot
fig = plt.figure()
plt.title('Detected sound fit to sine wave for 300n solenoid')
plt.ylabel('Voltage [V]')
plt.xlabel('Time [s]')
plt.scatter(time2, v2, color="red", label="300n oscilloscope data")

guesses2 = [0.01, ang_freq, 0]
popt2, pcov2 = curve_fit(sin, time2, v2, p0=guesses2) 
plt.plot(time2, sin(time2, *popt2), 'r-', color="orange", label=f"{popt2[0]:.9f}*sin({popt2[1]:.9f}t + {popt2[2]:.9f}")

plt.legend()

# 93n plot
fig = plt.figure()
plt.title('Detected sound fit to sine wave for 93 solenoid')
plt.ylabel('Voltage [V]')
plt.xlabel('Time [s]')
plt.scatter(time1, v1, color="green", label="93n oscilloscope data")

guesses3 = [0.01, ang_freq, 0]
popt3, pcov3 = curve_fit(sin, time3, v3, p0=guesses3) 
plt.plot(time3, sin(time3, *popt3), 'r-', color="orange", label=f"{popt3[0]:.9f}*sin({popt3[1]:.9f}t + {popt3[2]:.9f}")

plt.legend()

# normalized residuals
fig = plt.figure()
plt.title('Normalized residuals for 140n')
plt.ylabel('Residuals [V]')
plt.xlabel('Time [s]')
fit1 = popt1[0]*np.sin(popt1[1]*time1 + popt1[2]) 
plt.scatter(time1, (fit1-v1)/popt1[0], color='blue')
print(f"140n: {np.abs(np.mean(np.abs(fit1-v1)/popt1[0]))}")

fig = plt.figure()
plt.title('Normalized residuals for 300n')
plt.ylabel('Residuals [V]')
plt.xlabel('Time [s]')
fit2 = popt2[0]*np.sin(popt2[1]*time2 + popt2[2]) 
plt.scatter(time2, (fit2-v2)/popt2[0], color='red')
print(f"300n: {np.abs(np.mean(np.abs(fit2-v2)/popt2[0]))}")

fig = plt.figure()
plt.title('Normalized residuals for 93n')
plt.ylabel('Residuals [V]')
plt.xlabel('Time [s]')
fit3 = popt3[0]*np.sin(popt3[1]*time3 + popt3[2]) 
plt.scatter(time3, (fit3-v3)/popt3[0], color='green')
print(f"93n: {np.abs(np.mean(np.abs(fit3-v3)/popt3[0]))}")

plt.show()
