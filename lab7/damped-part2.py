import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# get arrays
file = "./pt2-t4-cut.csv"
df = pd.read_csv(file)
acc = df['yaccelerometer'].to_numpy()
time = df['time'].to_numpy()

# damped function
def damped(t, amp, freq, damp_r, phase, offset):
    return amp * -1 * (freq**2) * np.exp(-damp_r * t) * np.cos(freq * t + phase) + offset

# set up plots
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_xlabel("Displacement [m]")
ax1.set_ylabel("Force [N]")
ax1.set_title("Displacement vs Force")
ax2.set_xlabel("Displacement [m]")
ax2.set_ylabel("Residuals [N]")
ax2.set_title("Residuals Plot")

# approx for function
guesses = [5, 13.5, 0.01, 0.1, 0]

# oscillation plot
popt, pcov = curve_fit(damped, time, acc, p0=guesses)
ax1.plot(time, damped(time, *popt), 'r-', label = "Fitted damped oscillation function")
ax1.scatter(time, acc)
ax1.legend()

# residuals plot
yfit = popt[0] * -1 * (popt[1]**2) * np.exp(-popt[2] * time) * np.cos(popt[1] * time + popt[3]) + popt[4]
ax2.scatter(time, acc-yfit)

# frequency & damping factor
print(f"The damped oscillation frequency: {popt[1]:.9f} 1/s")
print(f"The damping factor: {popt[2]:.9f} N*s/m")

plt.show()
