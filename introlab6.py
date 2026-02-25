import matplotlib.pyplot as plt
import numpy as np

period_sq = np.array([1.552, 2.224, 3.821, 5.430, 6.993, 8.728])
mo_inertia = np.array([2.538e-5, 3.552e-5, 5.581e-5, 7.610e-5, 9.639e-5, 1.167e-4])
error = np.array([1.871e-7, 3.108e-7, 1.440e-7, 1.515e-7, 1.821e-7, 4.103e-7])

fig = plt.figure()
plt.xlabel("Period^2 [s^2]")
plt.ylabel("Total Moment of Inertia [kg*m^2]")
plt.title("Total Moment of Inertia vs Period Squared (Torsional Pendulum)")

coef = np.polyfit(period_sq, mo_inertia, 1)


lin_func = np.poly1d(coef)
yfit = lin_func(period_sq)

plt.errorbar(period_sq, mo_inertia, yerr=error, fmt=".")

plt.plot(period_sq, yfit, label=f"y={coef[0]}x + {coef[1]}")

text = "+/- y-error for the 6 data points, left to right: 1.871e-7, 3.108e-7, 1.440e-7, 1.515e-7, 1.821e-7, 4.103e-7 [kg*m^2]"
plt.figtext(0.5, 0.01, text, wrap=True, horizontalalignment='center')

plt.legend()
plt.show()
