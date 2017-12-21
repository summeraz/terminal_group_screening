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
cof_alkane_crystalline = [0.196, 0.140, 0.117, 0.089, 0.110, 0.075]
err_alkane_crystalline = [0.138, 0.070, 0.038, 0.033, 0.028, 0.022]
cof_alkane_amorphous = [0.152, 0.147, 0.152, 0.151, 0.137, 0.148]
err_alkane_amorphous = [0.003, 0.007, 0.007, 0.007, 0.008, 0.006]
cof_peg_crystalline = [0.099, 0.143, 0.133, 0.125, 0.138, 0.134]
err_peg_crystalline = [0.011, 0.002, 0.008, 0.004, 0.003, 0.003]
cof_peg_amorphous = [0.156, 0.144, 0.132, 0.131, 0.131, 0.128]
err_peg_amorphous = [0.005, 0.007, 0.003, 0.009, 0.004, 0.005]

ax.errorbar(chainlength, cof_alkane_crystalline, yerr=err_alkane_crystalline,
            marker='o', linewidth=5, label='Alkane, crystalline', color=colors[1])
ax.errorbar(chainlength, cof_alkane_amorphous, yerr=err_alkane_amorphous,
            marker='s', linewidth=5, label='Alkane, amorphous', color=colors[4])
ax.errorbar(chainlength, cof_peg_crystalline, yerr=err_peg_crystalline,
            marker='^', linewidth=5, label='PEG, crystalline', color=colors[6])
ax.errorbar(chainlength, cof_peg_amorphous, yerr=err_peg_amorphous,
            marker='d', linewidth=5, label='PEG, amorphous', color=colors[9])

plt.xlabel('Chain length')
ax.set_ylabel('Coefficient of friction')
plt.xlim([6, 23])
plt.ylim([0.00, 0.25])
plt.xticks([7, 10, 13, 16, 19, 22])
plt.legend()
plt.tight_layout()
plt.savefig('Trevor-cof-chainlength.pdf')
