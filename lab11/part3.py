import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from scipy.optimize import curve_fit

# data
mass = 50e-3 #kg
freq = 30 #Hz
length = np.array([0.214, 0.399, 0.542, 0.726, 0.897, 1.094, 1.294]) #m
len_err = np.array([0.01, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02]) #m
h_num = np.array([1, 2, 3, 4, 5, 6, 7])

# calc
tension = mass * 9.8

# plot setup
fig = plt.figure()
plt.title('')
plt.xlabel('')
plt.ylabel('')

coef = np.polyfit(h_num, length, 1)
lin_func = np.poly1d(coef)
yfit = lin_func(h_num)

result = linregress(h_num, length)

plt.errorbar(h_num, length, fmt=".", yerr = len_err)
plt.plot(h_num, yfit, label=f"y = ({coef[0]:.9f} +/- {result.stderr:.9f})x + ({coef[1]:.9f} +/- {result.intercept_stderr:.9f})")

plt.legend()


# residuals
fig = plt.figure()
plt.title("")
plt.xlabel("")
plt.ylabel("")
plt.scatter(h_num, yfit - length)

# agreement tests
mass_overall = 11e-3 #kg
length_overall = 2.232 #m
ten_err = 0.5e-3*9.8
th_d = mass_overall / length_overall
th_d_err = th_d * np.sqrt(((0.5e-3/mass_overall)**2) + ((0.0005/length_overall)**2))
exp_d = (1/(2*freq*coef[0])**2)*(tension)
exp_d_err = exp_d * np.sqrt(((ten_err/tension)**2) + ((2 * result.stderr / coef[0])**2))
print(f"TH Linear mass density: {th_d:.9f} +/- {th_d_err:.9f}")
print(f"EXP Linear mass density: {exp_d:.9f} +/- {exp_d_err:.9f}")
print(f"Values agree? They agree if A - B ({abs(exp_d - th_d):.9f}) < 2(err_a^2 + err_b^2) ({2*((exp_d_err**2) + (th_d_err**2)):.9f})")
print(f"Values agree? {abs(exp_d - th_d) < 2*((th_d_err**2) + (exp_d_err**2))}")

"""
# reduced chi squared
error = np.std(length)/np.sqrt(len(length))
chi_sq = np.sum(((length-yfit) / error) **2)
red_chi_sq = chi_sq / (len(length) - 2)
"""
plt.show()
