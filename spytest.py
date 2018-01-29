"""
SCript to test spyder

@author: bjk1y13
"""

print( "Hello")

x = 5

print(x)

import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(-1, 4, 101)
y = np.exp(-x)#*np.sin(np.pi*x)
plt.plot(x,y)
plt.title('First test of Spyder')
#plt.savefig('tmp.png')
plt.show()