import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sp


def func(phi, y0, A, w , xc):
    return y0 + (A / w / np.sqrt(np.pi/2)) * np.exp( -2 * (phi - xc) / w**2 )


def recouvrement(d, R, phi):
    phi = np.radians(phi)
    print(phi)
    premier = 2 * R**2 * np.arccos(d / (2*R) * np.tan(phi))
    deuxieme = d*R*np.tan(phi)*np.sin(np.arccos(d / (2*R) * np.tan(phi)))
    return premier - deuxieme

nbCoups = np.array([25, 60, 368, 806, 1321, 1257, 830, 326, 53, 21, 24]) #coups/min
background = 7 # coups/min
nbCoups = nbCoups - background

angles = np.array([-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20])


# sp.curve_fit(func, np.abs(angles), nbCoups, p0 = [])

fig, ax = plt.subplots(1, 1)
ax.scatter(angles, nbCoups)

d = 15
R = 5.08/2
phi_1 =  np.linspace(-30, 30, 600)
phi_2 = np.abs(phi_1)
y_values = recouvrement(d, R, phi_2)/recouvrement(d, R, 0)

ax.plot(phi_1, y_values)


plt.show()