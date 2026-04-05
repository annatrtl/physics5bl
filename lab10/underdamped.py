import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from scipy.optimize import curve_fit

# data
ampl = np.array([3.6, -2.72, 2.0, -1.52, 1.12, -0.8, 0.64, -0.48, 0.4, -0.32, 0.26, -0.16]) #V
time = np.array([0.168, 0.488, 0.816, 1.14, 1.46, 1.80, 2.12, 2.44, 2.78, 3.10, 3.42, 3.74]) #ms
freq = 10 #Hz

# calc
time = time*(10e-3)
w_freq = 2*np.pi*freq

# underdamped fit
def under(t, amp, w, a, phi):
    return amp * np.exp(-1*a*t)*np.cos(w*t - phi)


# plot setup
fig = plt.figure()
plt.title('RLC Underdamped Transient Response')
plt.xlabel('Voltage Amplitudes [V]')
plt.ylabel('Time difference (from edge of wave impulse) [s]')
plt.errorbar(time, ampl, fmt='.')
guesses = [2.5, 1e-2, 0.5e-2, 0]

# plot
popt, pcov = curve_fit(under, time, ampl, p0=guesses)
plt.plot(time, under(time, *popt), '-r', label=f"Fitted function")


a_err = np.sqrt(np.diag(pcov))[2]
w_err = np.sqrt(np.diag(pcov))[1]
#text=f"a = {popt[2]:.9f} +/- {a_err:.9f} 1/s, w_o = {popt[1]:.9f} +/- {w_err:.9f} 1/s"
#fig = fig.text(0.5, 0.02, text, wrap=True, horizontalalignment='center')
plt.legend()

# a & w 
print(f"a: {popt[2]:.9f} +/- {a_err:.9f} 1/s")
print(f"w: {popt[1]:.9f} +/- {w_err:.9f} 1/s")

# agreement tests
induc = 100e-3 #H
capac = 0.1e-6 #F
resist = 50 #ohm
i_err = 0.1*induc
c_err = 0.1*capac
r_err = (100*0.05)/ 2

th_w = 1 / np.sqrt(induc*capac)
th_w_err = (th_w / 2) * np.sqrt((i_err**2/induc**2) + (c_err**2/capac**2))


th_a = resist / (2 * induc)
th_a_err = th_a * np.sqrt((r_err**2/resist**2) + (i_err**2/induc**2))


print(f"Values agree for a? They agree if A - B ({abs(popt[2] - th_a):.9f}) < 2(aA + aB) ({2*((a_err**2) + (th_a_err**2)):.9f})")
print(f"Values agree for a? {abs(popt[2] - th_a) < 2*((a_err**2) + (th_a_err**2))}")

print(f"Values agree for w? They agree if A - B ({abs(popt[1] - th_w):.9f}) < 2(aA + aB) ({2*((w_err**2) + (th_w_err**2)):.9f})")
print(f"Values agree for w? {abs(popt[1] - th_w) < 2*((w_err**2) + (th_w_err**2))}")


# residuals
fig = plt.figure()
plt.title("Residuals for Underdamped Plot")
plt.xlabel("Time difference (from edge of wave impulse) [s]")
plt.ylabel("Residuals [V]")
yfit = under(time, *popt)
plt.scatter(time, yfit - ampl)


plt.show()
