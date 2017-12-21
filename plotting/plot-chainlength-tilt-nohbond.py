import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)
chainlengths = df.chainlength.unique()
chainlengths.sort()
terminal_groups = df.terminal_group.unique()
terminal_groups.sort()
n_groups = len(terminal_groups)

hbonding_groups = ['amino', 'carboxyl', 'hydroxyl']

fig = plt.figure(1)
ax = plt.subplot(111)

hsv = plt.get_cmap('hsv')
colors = hsv(np.linspace(0, 1.0, len(terminal_groups)+1))
markers = ['o', 's', '^', 'd', 'P']

all_chainlengths = []
all_tilt = []

for i, terminal_group in enumerate(terminal_groups):
    if terminal_group not in hbonding_groups:
        chainlengths = []
        tilts = []
        for job in project.find_jobs({'terminal_group': terminal_group}):
            chainlength = job.sp['chainlength']
            tilt = job.document['tilt']['15nN']
            chainlengths.append(chainlength)
            all_chainlengths.append(chainlength)
            tilts.append(tilt)
            all_tilt.append(tilt)
        ax.scatter(chainlengths, tilts, color=colors[i],
                   marker='o', s=120)

slope, intercept, r_val, p_val, err = stats.linregress(all_chainlengths, all_tilt)
xrange = np.max(all_chainlengths) - np.min(all_chainlengths)
xs = [np.min(all_chainlengths) - xrange * 0.02, np.max(all_chainlengths) + xrange * 0.02]
yrange = np.max(all_tilt) - np.min(all_tilt)
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=2)
print(r_val, p_val)

plt.xlabel('Chain length')
ax.set_ylabel('Average tilt angle, degrees')
plt.xlim(np.min(all_chainlengths) - xrange * 0.02, np.max(all_chainlengths) + xrange * 0.02)
plt.ylim(np.min(all_tilt) - yrange * 0.02, np.max(all_tilt) + yrange * 0.02)
plt.tight_layout()
plt.savefig('chainlength-tilt-nohbond.pdf')
