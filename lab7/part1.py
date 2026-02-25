import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd

# get arrays
file = "./pt1-t2-cut.csv"
df = pd.read_csv(file)
displ = df['displacement'].to_numpy()
displ = -1*displ # fit to f = -kx
force = df['force'].to_numpy()


#uncertainty in spring const. ak
result = linregress(displ, force)
stderr = result.stderr

# set up plots
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_xlabel("Displacement [m]")
ax1.set_ylabel("Force [N]")
ax1.set_title("Displacement vs Force")
ax2.set_xlabel("Displacement [m]")
ax2.set_ylabel("Residuals [N]")
ax2.set_title("Residuals Plot")

# least squares calc
coef = np.polyfit(displ, force, 1)
lin_func = np.poly1d(coef)
yfit = lin_func(displ)

# acceptance test
print(f"Values agree? They agree if A - B ({abs(coef[0] - 12):.3f}) < 2(aA + aB) ({2*(stderr + 1.2):.3f})")
print(f"Values agree? {abs(coef[0] - 12) < 2*(stderr + 1.2)}")

# least squares plot
ax1.scatter(displ, force, c='orange')
ax1.plot(displ, yfit, label=f"y={coef[0]}x + {coef[1]}")

# display uncertainty
text = f"Uncertainty for slope: {stderr} [N/m]"
plt.text(0.5, -0.1, text, wrap=True, horizontalalignment='center',transform=ax1.transAxes)

ax1.legend()

# residuals plot
y_vals = coef[0]*displ
ax2.scatter(displ, y_vals - force)

plt.show()
