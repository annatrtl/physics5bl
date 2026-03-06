import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# get arrays
file = "./pt2-t4-cut.csv"
df = pd.read_csv(file)
acc = df['yaccelerometer'].to_numpy()
force = df['force'].to_numpy()
time = df['time'].to_numpy()

# harmonic function
def harmonic(t, amp, freq, phase, offset):
    return amp * -1 *(freq**2) * np.cos(freq * t + phase) + offset

# set up plots
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Y Acceleration [1/s^2]")
ax1.set_title("Y Acceleration vs Time fitted to Harmonic Oscillation")
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Residuals [1/s^2]")
ax2.set_title("Residuals Plot")

# approx for function
guesses = [5, 8, 1, -10]

# oscillation plot
popt, pcov = curve_fit(harmonic, time, acc, p0=guesses)
ax1.plot(time, harmonic(time, *popt), 'r-', label = "Fitted harmonic oscillation function")
ax1.scatter(time, acc)
ax1.legend()

# residuals plot
yfit = popt[0] * -1 * (popt[1]**2) * np.cos(popt[1] * time + popt[2]) + popt[3]
ax2.scatter(time, acc - yfit)

# frequency & spring constant
mass = 0.203
m_err = 0.001
f_err = np.sqrt(np.diag(pcov))[1]
print(f"The harmonic oscillation frequency: {popt[1]:.9f} +/- {f_err:.9f} 1/s")
k_err = (popt[1]**2)*mass*np.sqrt(4*(f_err**2/popt[1]**2) + (m_err**2/mass**2))
print(f"The spring constant: {(popt[1]**2)*mass:.9f} +/- {k_err:.9f} N/m")


# acceptance test
print(f"Value agree? They agree if A - B ({abs(((popt[1]**2)*mass) - 12):.3f}) < 2(aA + aB) ({2*((k_err**2) + (1.2**2)):.3f})")
print(f"Values agree? {abs(((popt[1]**2)*mass) - 12) < (2*((k_err**2) + (1.2**2)))}")
plt.show()
