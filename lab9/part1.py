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
ps_angle = ps*(0.001)*freq*(360) 
vc_over_vo = vc/vo

# vc/vo function fit
def v_ratio_func(x, a, t):
    return (a / ((1 + (x**2)*(t**2)) ** 0.5))

# phase shift function fit
def ps_func(x, t):
    return np.arctan(-1*x*t) * (180/np.pi)

# plot 1: vc/vo vs ang_freq plot setup
fig = plt.figure()
plt.title('Vc/Vo as a function of Angular Frequency (Log-Log)')
plt.xlabel('Log Scale Angular Frequency [rad/s]')
plt.ylabel('Log Scale Vc/Vo')
plt.errorbar(np.log(ang_freq), np.log(vc_over_vo), fmt='.')
r_guesses = [1, 1e-3]

# plot 1
popt_r, pcov_r = curve_fit(v_ratio_func, ang_freq, vc_over_vo, p0=r_guesses)
plt.plot(np.log(ang_freq), np.log(v_ratio_func(ang_freq, *popt_r)), '-r', label=f"Fitted function")

# plot 1: amplitude & time constant values
a_err = np.sqrt(np.diag(pcov_r))[0]
r_t_err = np.sqrt(np.diag(pcov_r))[1]
text1=f"The amplitude constant: {popt_r[0]:.9f} +/- {a_err:.9f} volts. The time constant: {popt_r[1]:.9f} +/- {r_t_err:.9f} sec."
fig = fig.text(0.5, 0.02, text1, wrap=True, horizontalalignment='center')
plt.legend()

# plot 1: residuals
yfit1 = v_ratio_func(ang_freq[:-1], popt_r[0], popt_r[1])
fig = plt.figure()
plt.title('Residuals for Vc/Vo vs Angular Frequency plot')
plt.xlabel('Angular Frequency [1/s]')
plt.ylabel('Vc/Vo Residuals')
plt.scatter(ang_freq[:-1], yfit1 - vc_over_vo[:-1])

# plot 2: ps_ang vs ang_freq plot setup
fig = plt.figure()
plt.title('Phase Shift as a function of Log Scale Angular Frequency')
plt.xlabel('Log Scale Angular Frequency [1/s]')
plt.ylabel('Phase Shift [degrees]')
plt.errorbar(np.log(ang_freq), ps_angle, fmt='.')
ps_guesses = [-1e-3]

# plot 2
popt_ps, pcov_ps = curve_fit(ps_func, ang_freq, ps_angle, p0=ps_guesses)
plt.plot(np.log(ang_freq), ps_func(ang_freq, *popt_ps), '-r', label=f"Fitted function")

# plot 2: time constant value
ps_t_err = np.sqrt(np.diag(pcov_ps))[0]
text2=f"The time constant: {popt_ps[0]:.9f} +/- {ps_t_err:.9f} sec."
fig = fig.text(0.5, 0.02, text2, wrap=True, horizontalalignment='center')
plt.legend()


# plot 2: residuals
yfit2 = ps_func(ang_freq[:-1], popt_ps[0])
fig = plt.figure()
plt.title('Residuals for Phase Shift vs Angular Frequency plot')
plt.xlabel('Angular Frequency [rad/s]')
plt.ylabel('Phase shift residuals')
plt.scatter(ang_freq[:-1], yfit2 - ps_angle[:-1])

# amplitude & time constant 
print(f"The amplitude constant: {popt_r[0]:.9f} +/- {a_err:.9f} volts")
print(f"The time constant: {popt_r[1]:.9f} +/- {r_t_err:.9f} sec")

# agreement test
t_acc_err = 1e-3*np.sqrt((10/1000)**2 + ((1e-6*0.05/(1e-6))**2))
print(t_acc_err)
print(f"Values agree for time constant? They agree if A - B ({abs(popt_r[1] - 1e-3):.9f}) < 2(aA + aB) ({2*((r_t_err**2) + (t_acc_err**2)):.9f})")
print(f"Values agree time constant? {abs(popt_r[1] - 1e-3) < 2*((r_t_err**2) + (t_acc_err**2))}")

plt.show()


