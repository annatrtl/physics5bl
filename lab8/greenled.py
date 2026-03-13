import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# data
dac_voltage = np.array([0.104, 0.530, 0.836, 1.265, 1.588, 2.010, 2.321, 2.748, 2.964, 3.292])
high_gain_1ohm = np.array([-0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, 0.016e-3, 0.036e-3, 0.062e-3])

# calcs
ten_kohm_voltage = dac_voltage - high_gain_1ohm
offset = -0.19e-3/-2.01
current = (high_gain_1ohm + offset) / 1 #volts/ohms

# exponential function
def expf(x, a, b, c):
    return a * np.exp(b*x) + c 

# approx for function
guesses = [0.01, 1, 0.00005]

# I vs V plot
fig = plt.figure()
plt.xlabel("Voltage corrected for offset [Volts]")
plt.ylabel("Current [Amps]")
plt.errorbar(ten_kohm_voltage, current, fmt=".")

popt, pcov = curve_fit(expf, ten_kohm_voltage, current, p0=guesses) 
plt.plot(ten_kohm_voltage, expf(ten_kohm_voltage, *popt), 'r-', label=f"Fitted exponential function")
plt.legend()

# residuals plot
fig = plt.figure()
plt.xlabel("Voltage corrected for offset [Volts]")
plt.ylabel("Residuals [Amps]")

yfit = popt[0] * np.exp(popt[1] * ten_kohm_voltage) + popt[2]
plt.scatter(ten_kohm_voltage, yfit - current)
print(popt)

plt.show()

