import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["grid.linewidth"] = 2.5
plt.rcParams["xtick.labelsize"] = 34
plt.rcParams["ytick.labelsize"] = 34
plt.rcParams["axes.labelsize"] = 38
plt.rcParams["lines.markersize"] = 18
plt.rcParams["legend.fancybox"] = True
plt.rcParams["legend.fontsize"] = 27

hsv = plt.get_cmap('nipy_spectral')
colors = hsv(np.linspace(0, 1.0, 10))

fig, ax = plt.subplots(figsize=(12,9))

chainlength = [7, 10, 13, 16, 19, 22]
s2_alkane_crystalline = [0.98, 0.99, 0.994, 0.997, 0.9975, 0.998]
err_alkane_crystalline = [0.005, 0.001, 0.0001, 0.0001, 0.0001, 0.0001]
s2_alkane_amorphous = [0.72, 0.85, 0.92, 0.94, 0.96, 0.965]
err_alkane_amorphous = [0.025, 0.02, 0.005, 0.005, 0.001, 0.001]
s2_peg_crystalline = [0.86, 0.905, 0.94, 0.96, 0.97, 0.975]
err_peg_crystalline = [0.026, 0.01, 0.0075, 0.002, 0.001, 0.001]
s2_peg_amorphous = [0.6, 0.715, 0.835, 0.87, 0.9, 0.92]
err_peg_amorphous = [0.03, 0.018, 0.013, 0.007, 0.002, 0.001]

ax.errorbar(chainlength, s2_alkane_crystalline, yerr=err_alkane_crystalline,
            marker='o', linewidth=5, label='Alkane, crystalline', color=colors[1])
ax.errorbar(chainlength, s2_alkane_amorphous, yerr=err_alkane_amorphous,
            marker='s', linewidth=5, label='Alkane, amorphous', color=colors[4])
ax.errorbar(chainlength, s2_peg_crystalline, yerr=err_peg_crystalline,
            marker='^', linewidth=5, label='PEG, crystalline', color=colors[6])
ax.errorbar(chainlength, s2_peg_amorphous, yerr=err_peg_amorphous,
            marker='d', linewidth=5, label='PEG, amorphous', color=colors[9])

plt.xlabel('Chain length')
ax.set_ylabel('Nematic order')
plt.xlim([6, 23])
plt.ylim([0.5, 1.0])
plt.xticks([7, 10, 13, 16, 19, 22])
#plt.legend()
plt.tight_layout()
plt.savefig('Trevor-s2-chainlength.pdf')
