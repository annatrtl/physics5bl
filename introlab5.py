import matplotlib.pyplot as plt
import numpy as np

normal = np.array([0.441, 0.735, 1.029, 1.127, 1.323, 1.568])
static_fric = np.array([1.16, 1.33, 1.31, 1.41, 1.53, 1.45])
error = np.array([0.017, 0.040, 0.017, 0.011, 0.031, 0.035])

fig = plt.figure()
plt.xlabel("Normal Force (N)")
plt.ylabel("Max. Static Friction Force (N)")
plt.title("Max Static Friction Force vs Normal Force (Cork & Wood)")

coef = np.polyfit(normal, static_fric, 1)

print(coef) #slope, y-intercept

lin_func = np.poly1d(coef)
yfit = lin_func(normal)

plt.errorbar(normal, static_fric, yerr=error, fmt=".")

plt.plot(normal, yfit, label=f"Linear Regression; (slope, y-intercept: {coef})")

plt.legend()
plt.show()
