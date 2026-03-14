import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
from scipy.stats import linregress

# data
#dac_voltage = np.array([0.104, 0.530, 0.836, 1.265, 1.588, 2.010, 2.321, 2.748, 2.964, 3.292])
#high_gain_1ohm = np.array([-0.035e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.034e-3, -0.033e-3, 0.016e-3, 0.036e-3, 0.062e-3])
file = "./datagreenled.csv"
df = pd.read_csv(file)
dac_voltage = df['dac'].to_numpy()
high_gain_1ohm = df['highgain'].to_numpy()
high_gain_1ohm = high_gain_1ohm*1e-3

# calcs
ten_kohm_voltage = dac_voltage - high_gain_1ohm
offset = -0.11e-3/-2.04
current = (high_gain_1ohm + offset) / 1 #volts/ohms

# exponential function
def expf(x, a, b, c):
    return a * np.exp(b*x) + c 

# approx for function
guesses = [0, 1, 0]

# linear fit
coef = np.polyfit(ten_kohm_voltage, current, 1)
lin_func = np.poly1d(coef)
linfit = lin_func(ten_kohm_voltage)
result = linregress(ten_kohm_voltage, current)

# I vs V plot
fig = plt.figure()
plt.title("Current vs Voltage for Green LED")
plt.xlabel("Voltage corrected for offset [V]")
plt.ylabel("Current [A]")
plt.errorbar(ten_kohm_voltage, current, fmt=".")

popt, pcov = curve_fit(expf, ten_kohm_voltage, current, p0=guesses) 
plt.plot(ten_kohm_voltage, expf(ten_kohm_voltage, *popt), 'r-', label=f"Exponential fit")
plt.plot(ten_kohm_voltage, linfit, label=f"y = ({coef[0]:.9f} +/- {result.stderr:.9f})x + ({coef[1]:.9f} +/- {result.intercept_stderr:.9f})")
plt.legend()

# resistance value
r = 1/coef[0]
err = r * result.stderr
print(f"Resistance: {r:.9f} +/- {err:.9f}")

# chi squared
c_err = np.std(current)/np.sqrt(len(current))
chi_sq = np.sum(((current-linfit) / c_err) **2)
red_chi_sq = chi_sq / (len(ten_kohm_voltage) - 2)
text = f"Reduced chi squared: {red_chi_sq:.9f}"
fig = fig.text(0.5, 0.02, text, wrap=True, horizontalalignment='center')

# residuals plot
fig = plt.figure()
plt.title("Residuals for Green LED")
plt.xlabel("Voltage corrected for offset [V]")
plt.ylabel("Residuals [A]")

yfit = popt[0] * np.exp(popt[1] * ten_kohm_voltage) + popt[2]
#plt.scatter(ten_kohm_voltage, yfit - current, label="Exponential residuals", color="blue")
plt.scatter(ten_kohm_voltage, linfit - current, label="Linear residuals", color="orange")

plt.legend()
plt.show()

