import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd

# data
file = './t7-cut.csv'
df = pd.read_csv(file)
voltage = df['v'].to_numpy() #mV
bz = df['bz'].to_numpy() #microT
time = df['time'].to_numpy() #s

# calc
voltage = voltage * 1e-3
bz = bz * 1e-6
dBdt = [(bz[i+1]-bz[i-1])/(time[i+1]-time[i-1]) for i in range(1, len(bz)-1)]
dBdt = np.insert(dBdt, 0, bz[1]-bz[0])/(time[1]-time[0])
dBdt = np.append(dBdt, bz[-1]-bz[-2])/(time[-1]-time[-2])

# plot setup
fig = plt.figure()
plt.title('EMF as a function of dBz/dt')
plt.xlabel('Derivative of the z-component of magnetic field [T/s]')
plt.ylabel('EMF [V]')

coef = np.polyfit(dBdt, voltage, 1)
lin_func = np.poly1d(coef)
yfit = lin_func(dBdt)

result = linregress(dBdt, voltage)

plt.errorbar(dBdt, voltage, fmt=".")
plt.plot(dBdt, yfit, label=f"y = ({coef[0]:.9f} +/- {result.stderr:.9f})x + ({coef[1]:.9f} +/- {result.intercept_stderr:.9f})")
plt.legend()

# residuals plot
fig = plt.figure()
plt.title('Residuals for the EMF vs dBz/dt plot')
plt.xlabel('Derivative of the z-component of magnetic field [T/s]')
plt.ylabel('Residuals [V]')

plt.scatter(dBdt, yfit - voltage)

# predicted slope
n = 21
d = 2.3 * 1e-2 #m
a = np.pi * ((d/2)**2)
pr_slope = -1 * n * a
pr_slope_err = pr_slope * 0.05e-3
print(pr_slope, pr_slope_err)
print(coef[0], result.stderr)

print(f"Values agree? They agree if A - B ({abs(pr_slope - coef[0]):.9f}) < 2(err_a^2 + err_b^2) ({2*((pr_slope_err**2) + (result.stderr**2)):.9f})")
print(f"Values agree? {abs(pr_slope - coef[0]) < 2*((pr_slope_err**2) + (result.stderr**2))}")

plt.show()

