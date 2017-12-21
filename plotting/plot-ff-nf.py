import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

ff = []
ff_err = []
nf = [5, 15, 25]
for load in nf:
    data = np.loadtxt('friction_{}nN.txt'.format(load))
    ff.append(np.mean(data[int(len(data)*0.8):,1]))
    ff_err.append(np.std(data[int(len(data)*0.8):,1]))

fig, ax = plt.subplots()

slope, intercept, r_val, p_val, err = stats.linregress(nf, ff)
xs = [-1.0, 30.0]
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=3)
ax.errorbar(nf, ff, linestyle='None', marker='^', markersize=25)

plt.xlabel('Normal force, nN', fontsize=32)
plt.ylabel('Friction force, nN', fontsize=32)
plt.xlim([0.0, 30.0])
plt.ylim([0.0, 5.5])
plt.tight_layout()
plt.savefig('ff-nf.pdf')
