import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Import slider package
from matplotlib.widgets import Slider


# Fermi-Dirac Distribution
def fermi(E: float, E_f: float, T: float) -> float:
    k_b = 8.617 * (10**-5) # eV/K
    return 1/(np.exp((E - E_f)/(k_b * T)) + 1)

# General plot parameters
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['ytick.major.width'] = 2

# Create figure and add axes
fig = plt.figure(figsize=(6, 4))
fig.tight_layout()
fig.subplots_adjust(bottom=0.2, top=0.75)
ax = fig.add_subplot(111)

# Create axes for sliders
ax_Ef = fig.add_axes([0.3, 0.85, 0.4, 0.05])
ax_Ef.spines['top'].set_visible(True)
ax_Ef.spines['right'].set_visible(True)
ax_T = fig.add_axes([0.3, 0.92, 0.4, 0.05])
ax_T.spines['top'].set_visible(True)
ax_T.spines['right'].set_visible(True)

# Create sliders
s_Ef = Slider(ax=ax_Ef, label='Fermi Energy ', valmin=0, valmax=1.0,valfmt=' %1.1f eV', facecolor='#cc7000')
s_T = Slider(ax=ax_T, label='Temperature ', valmin=100, valmax=1000, valinit=100, valfmt='%i K', facecolor='#cc7000')

# Plot default data
x = np.linspace(-0, 1, 100)
Ef_0 = 0.5
T_0 = 100
y = fermi(x, Ef_0, T_0)
f_d, = ax.plot(x, y, linewidth=2.5)

# Update values
def update(val):
    Ef = s_Ef.val
    T = s_T.val
    f_d.set_data(x, fermi(x, Ef, T))
    fig.canvas.draw_idle()

s_Ef.on_changed(update)
s_T.on_changed(update)


plt.show()