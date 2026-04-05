import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from scipy.optimize import curve_fit

# data
ampl = np.array([0.80, 1.58, 1.98, 2.27, 2.48, 2.68, 2.88, 3.60 ]) #V
time = np.array([18.6, 38.3, 58, 80.8, 100, 121, 164, 207]) #ms
freq = 10 #Hz

# calc
time = time*(10e-3)
ampl = ampl[-1] - ampl
ampl = ampl/ 2.0
w_freq = 2*np.pi*freq

# overdamped fit
def over(t, A, D):
    return A * np.exp(-1*D*t)


# plot setup
fig = plt.figure()
plt.title('RLC Overdamped Transient Response')
plt.xlabel('Voltage difference (from edge of wave impulse) [V]')
plt.ylabel('Time difference (from edge of wave impulse) [s]')
plt.errorbar(time, ampl, fmt='.')
guesses = [0.5, 1e-3]

# plot
popt, pcov = curve_fit(over, time, ampl, p0=guesses)
plt.plot(time, over(time, *popt), '-r', label=f"Fitted function")

D_err = np.sqrt(np.diag(pcov))[1]
#text=f"D = {popt[1]:.9f} +/- {D_err:.9f}"
#fig = fig.text(0.5, 0.02, text, wrap=True, horizontalalignment='center')
plt.legend()


# a & w 
print(f"D: {popt[1]:.9f} +/- {D_err:.9f} 1/s")

# agreement tests
induc = 100e-3 #H
capac = 47e-6 #F
resist = 1e3 #ohm
i_err = 0.1*induc
c_err = 0.2*capac
r_err = 0.05*resist

th_w = 1 / np.sqrt(induc*capac)
th_w_err = (th_w / 2) * np.sqrt((i_err**2/induc**2) + (c_err**2/capac**2))


th_a = resist / (2 * induc)
th_a_err = th_a * np.sqrt((r_err**2/resist**2) + (i_err**2/induc**2))

th_b = np.sqrt((th_a**2) - (th_w**2))
th_b_err = (1/th_b) * np.sqrt((th_a**2)*(th_a_err**2) + (th_w**2)*(th_w_err**2))



sub = th_a - th_b
term1 = (1/2*induc)*(1-(th_a/th_b))*r_err
term2 = (-1*(resist/2*induc*induc)*(1-(th_a/th_b)) - (th_w*th_w/(2*induc*th_b)))*i_err
term3 = (-1*th_w*th_w/(2*capac*th_b))*c_err
sub_err = np.sqrt((term1**2)+(term2**2)+(term3**2))


print(f"Values agree for sub? They agree if A - B ({abs(popt[1] - sub):.9f}) < 2(aA + aB) ({2*((D_err**2) + (sub_err**2)):.9f})")
print(f"Values agree for sub? {abs(popt[1] - sub) < 2*((D_err**2) + (sub_err**2))}")


# residuals
fig = plt.figure()
plt.title("Residuals for Overdamped Plot")
plt.xlabel("Time difference (from edge of wave impulse) [s]")
plt.ylabel("Residuals [V]")
yfit = over(time, *popt)
plt.scatter(time, yfit - ampl)

plt.show()
