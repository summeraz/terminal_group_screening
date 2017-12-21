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

fig = plt.figure(1)
ax = plt.subplot(111)

hsv = plt.get_cmap('hsv')
colors = hsv(np.linspace(0, 1.0, len(terminal_groups)+1))
markers = ['o', 's', '^', 'd', 'P']

all_energies = []
all_intercepts = []

for i, terminal_group in enumerate(terminal_groups):
    for j, chainlength in enumerate(chainlengths):
        energies = []
        intercepts = []
        for job in project.find_jobs({'terminal_group': terminal_group,
                                      'chainlength': chainlength}):
            interaction_energy = job.document['shear_5nN_qq']
            energies.append(interaction_energy[0])
            all_energies.append(interaction_energy[0])
            intercepts.append(job.document['intercept'])
            all_intercepts.append(job.document['intercept'])
        ax.scatter(np.mean(energies), np.mean(intercepts), color=colors[i],
                   marker=markers[j], s=150)

slope, intercept, r_val, p_val, err = stats.linregress(all_energies, all_intercepts)
xs = [-3000, 1000]
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=2)
print(r_val)

plt.xlabel('Interaction energy (Coulomb), kJ/mol')
ax.set_ylabel('Intercept, nN')
plt.xlim([-3000, 1000])
plt.ylim([0, 6.75])
plt.tight_layout()
plt.savefig('interaction-energy-qq.pdf')
