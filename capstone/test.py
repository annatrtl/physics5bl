import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd

# data
#file = './TEK00000.csv' #noise data
#file = './TEK00001.csv' #test1 data
#file = './TEK00002.csv' #test2 data
#file = './300hz-140n.csv' 
#file = './300hz-300n.csv' 
#file = './300hz-93n.csv' 
file = './sweep300to900hz-93n.csv' 

df = pd.read_csv(file)
v = df['CH1'].to_numpy()
time = df['TIME'].to_numpy()


# plot
fig = plt.figure()
plt.title('')
plt.xlabel('')
plt.ylabel('')
plt.scatter(time, v)

plt.legend()
plt.show()
