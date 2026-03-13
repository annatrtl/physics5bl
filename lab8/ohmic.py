import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# data
dac_voltage = np.array([0.103, 0.526, 0.834, 1.260, 1.580, 2.006, 2.316, 2.736, 2.950, 3.279])
high_gain_1ohm = np.array([-0.027e-3, 0.013e-3, 0.042e-3, 0.081e-3, 0.112e-3, 0.152e-3, 0.181e-3, 0.221e-3, 0.242e-3, 0.271e-3])

# calcs
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

plt.errorbar(ten_kohm_voltage, current, fmt=".")
plt.plot(ten_kohm_voltage, yfit, label=f"y = {coef[0]:.9f}x + {coef[1]:.9f}")
plt.legend()

#residuals plot
fig = plt.figure()
plt.title("Residuals for 10kohm I vs V plot")
plt.xlabel("Voltage corrected for offset [V]")
plt.ylabel("Residuals [A]")

plt.scatter(ten_kohm_voltage, yfit - current)

plt.show()

