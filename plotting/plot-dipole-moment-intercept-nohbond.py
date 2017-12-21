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

all_dipoles = []
all_intercepts = []

for i, terminal_group in enumerate(terminal_groups):
    if terminal_group not in hbonding_groups:
        for j, chainlength in enumerate(chainlengths):
            dipoles = []
            intercepts = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                dipole_moment = job.document['dipole_moment']
                dipoles.append(dipole_moment)
                all_dipoles.append(dipole_moment)
                intercepts.append(job.document['intercept'])
                all_intercepts.append(job.document['intercept'])
            ax.scatter(np.mean(dipoles), np.mean(intercepts), color=colors[i],
                       marker=markers[j], s=150)

slope, intercept, r_val, p_val, err = stats.linregress(all_dipoles, all_intercepts)
xs = [-0.25, 6.5]
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=2)
print(r_val, p_val)

plt.xlabel('Dipole moment, Debye')
ax.set_ylabel('Intercept, nN')
plt.xlim([-0.25, 6.5])
plt.ylim([0, 4])
plt.tight_layout()
plt.savefig('dipole-moment-intercept-nohbond.pdf')
