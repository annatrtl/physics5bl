import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from scipy.optimize import curve_fit

# data
amp = np.array([3.6, -2.72, 2.0, -1.52, 1.12, -0.8, 0.64, -0.48, 0.4, -0.32, 0.26, -0.16]) #V
t = np.array([0.168, 0.488, 0.816, 1.14, 1.46, 1.80, 2.12, 2.44, 2.78, 3.10, 3.42, 3.74]) #ms
r = 72 #ohm
f = 10 #Hz

# calc
t = t*(10e-3)
current = amp / r
w = 2*np.pi*f

# underdamped fit
def under(t, amp, w, a, phi):
    return amp * np.exp(-1*a*t)*np.cos(w*t - phi)


# plot setup
fig = plt.figure()
plt.title('')
plt.xlabel('')
plt.ylabel('')
plt.errorbar(t, current, fmt='.')
guesses = [1e-3, 1e-3]

# plot
popt_r, pcov_r = curve_fit(under, t, amp, w, p0=guesses)
plt.plot(t, under(t, amp, w, *popt_r), '-r', label=f"Fitted function")

plt.legend()
plt.show()
