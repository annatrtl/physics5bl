import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from scipy.optimize import curve_fit

# data
mass = 50e-3 #kg
length = 1.357 #m
freq = np.array([14.7, 32.4, 44.9, 59.9, 75.1, 89.6]) #Hz
freq_err = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2]) #Hz
h_num = np.array([1, 2, 3, 4, 5, 6])

# calc
tension = mass * 9.8

# plot setup
fig = plt.figure()
plt.title('Fixed length and tension, varying frequency (inelastic string)')
plt.xlabel('Harmonic number')
plt.ylabel('Frequency [Hz]')

coef = np.polyfit(h_num, freq, 1)
lin_func = np.poly1d(coef)
yfit = lin_func(h_num)

result = linregress(h_num, freq)

plt.errorbar(h_num, freq, fmt=".", yerr = freq_err)
plt.plot(h_num, yfit, label=f"y = ({coef[0]:.9f} +/- {result.stderr:.9f})x + ({coef[1]:.9f} +/- {result.intercept_stderr:.9f})")
text = f"Error bars: {freq_err} Hz"
fig = fig.text(0.5, 0.02, text, wrap=True, horizontalalignment='center')

plt.legend()

# residuals
fig = plt.figure()
plt.title("Varying frequency residuals")
plt.xlabel("Harmonic number")
plt.ylabel("Frequency residuals [Hz]")
plt.scatter(h_num, yfit - freq)

# agreement tests
mass_overall = 1e-3 #kg
length_overall = 1.972 #m
ten_err = 0.5e-3*9.8
th_d = mass_overall / length_overall
th_d_err = th_d * np.sqrt(((0.5e-3/mass_overall)**2) + ((0.0005/length_overall)**2))
exp_d = (tension/(2*length*coef[0])**2)
exp_d_err = exp_d * np.sqrt(((ten_err/tension)**2) + ((2 * result.stderr / coef[0])**2))
print(f"TH Linear mass density: {th_d:.9f} +/- {th_d_err:.9f}")
print(f"EXP Linear mass density: {exp_d:.9f} +/- {exp_d_err:.9f}")
print(f"Values agree? They agree if A - B ({abs(exp_d - th_d):.9f}) < 2(err_a^2 + err_b^2) ({2*((exp_d_err**2) + (th_d_err**2)):.9f})")
print(f"Values agree? {abs(exp_d - th_d) < 2*((th_d_err**2) + (exp_d_err**2))}")

# reduced chi squared
chi_sq = np.sum(((freq-yfit) / freq_err) **2)
red_chi_sq = chi_sq / (len(freq) - 2)
print(f"Reduced chi squared: {red_chi_sq:.9f}")

plt.show()
