import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# data
freq = np.array([10, 50, 100, 250, 500, 1000, 10000]) #hz
vo = np.array([4, 4, 3.96, 3.88, 3.88, 3.84, 3.84]) #volts
vc = np.array([4, 3.80, 3.36, 2.08, 1.20, 600e-3, 640e-3]) #volts
ps = np.array([0, -0.78, -0.8, -0.6, -0.42, -232e-3, -252e-3]) #msec



# calc
ang_freq = 2*np.pi*freq
log_ang_freq = np.log(ang_freq)
ps_angle = ps*freq*(1) 

log_vc_over_vo = np.log(vc/vo)

# low-pass
def low_pass(x, a, t):
    return a / ((1 + (x**2)*(t**2)) ** 0.5)

# vc/vo vs ang_freq
fig = plt.figure()
plt.title('title')
plt.xlabel('Log Scale Angular Frequency [rad/s]')
plt.ylabel('Log Scale Vo/Vc')
plt.errorbar(log_ang_freq, log_vc_over_vo, fmt='.')

# fit
guesses = [-2, 1e-3]

popt, pcov = curve_fit(low_pass, log_ang_freq, log_vc_over_vo, p0=guesses)
plt.plot(log_ang_freq, low_pass(log_ang_freq, *popt), '-r', label=f"idk")

plt.legend()


# amplitude & time constant 
a_err = np.sqrt(np.diag(pcov))[0]
t_err = np.sqrt(np.diag(pcov))[1]

print(f"The amplitude constant: {popt[0]:.9f} +/- {a_err:.9f} volts")
print(f"The time constant: {popt[1]:.9f} +/- {t_err:.9f} sec")

# acceptance test
t_acc_err = 1e-3*np.sqrt((1000/10)**2 + ((1e-6/(0.05*1e-6))**2))
print(f"Values agree for time constant? They agree if A - B ({abs(popt[1] - 1e-3):.3f}) < 2(aA + aB) ({2*((t_err**2) + (t_acc_err)):.3f})")
print(f"Values agree time constant? {abs(popt[1] - 1e-3) < 2*((t_err**2) + (t_acc_err**2))}")

plt.show()


