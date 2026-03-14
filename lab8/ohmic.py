import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd

# data
#dac_voltage = np.array([0.103, 0.526, 0.834, 1.260, 1.580, 2.006, 2.316, 2.736, 2.950, 3.279])
#high_gain_1ohm = np.array([-0.027e-3, 0.013e-3, 0.042e-3, 0.081e-3, 0.112e-3, 0.152e-3, 0.181e-3, 0.221e-3, 0.242e-3, 0.271e-3])
file = "./10kohm.csv"
df = pd.read_csv(file)
dac_voltage = df['dac'].to_numpy()
high_gain_1ohm = df['highgain'].to_numpy()
high_gain_1ohm = high_gain_1ohm*1e-3

# high gain
ten_kohm_voltage = dac_voltage - high_gain_1ohm
offset = -0.19e-3/-2.01
current = (high_gain_1ohm + offset) / 1 #volts/ohms

# I vs V plot
fig = plt.figure()
plt.title("Current vs Voltage for 10kohm Resistor")
plt.xlabel("Voltage corrected for offset [V]")
plt.ylabel("Current [A]")

coef = np.polyfit(ten_kohm_voltage, current, 1)
lin_func = np.poly1d(coef)
yfit = lin_func(ten_kohm_voltage)

result = linregress(ten_kohm_voltage, current)

plt.errorbar(ten_kohm_voltage, current, fmt=".")
plt.plot(ten_kohm_voltage, yfit, label=f"y = ({coef[0]:.9f} +/- {result.stderr:.9f})x + ({coef[1]:.9f} +/- {result.intercept_stderr:.9f})")

# chi squared
chi_sq = np.sum(((current-yfit) / yfit) **2)
red_chi_sq = chi_sq / (len(ten_kohm_voltage) - 2)
text = f"Reduced chi squared: {red_chi_sq:.9f}"
fig = fig.text(0.5, 0.02, text, wrap=True, horizontalalignment='center')

plt.legend()

# resistance value
r = 1/coef[0]
err = r * result.stderr
print(f"Resistance: {r:.9f} +/- {err:.9f}")

# acceptance test
print(f"Values agree? They agree if A - B ({abs(r - 10000):.3f}) < 2(aA + aB) ({2*((err**2) + (500**2)):.3f})")
print(f"Values agree? {abs(r - 10000) < 2*((err**2) + (500**2))}")


# residuals plot
fig = plt.figure()
plt.title("Residuals for 10kohm I vs V plot")
plt.xlabel("Voltage corrected for offset [V]")
plt.ylabel("Residuals [A]")

plt.scatter(ten_kohm_voltage, yfit - current)

plt.show()

