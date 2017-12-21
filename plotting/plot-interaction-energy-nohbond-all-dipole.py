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

fig, ax = plt.subplots()

plasma = plt.get_cmap('plasma')
#colors = plasma(np.linspace(0, 1.0, len(terminal_groups)+1))
markers = ['o', 's', '^', 'd', 'P']


all_energies = []
all_intercepts = []

for i, terminal_group in enumerate(terminal_groups):
    if terminal_group not in hbonding_groups:
        for j, chainlength in enumerate(chainlengths):
            energies = []
            intercepts = []
            dipole = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                interaction_energy = job.document['shear_5nN_Etotal']
                all_energies.append(interaction_energy[0])
                energies.append(interaction_energy[0])
                all_intercepts.append(job.document['intercept'])
                intercepts.append(job.document['intercept'])
                dipole.append(job.document['dipole_moment'])
                sc = ax.scatter(energies, intercepts, c=dipole,
                                marker=markers[j], s=120, cmap=plasma,
                                vmin=0.0, vmax=7.0)

slope, intercept, r_val, p_val, err = stats.linregress(all_energies, all_intercepts)
xs = [-6000, 0]
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=2)
print(r_val, p_val)

plt.xlabel('Interaction energy, kJ/mol')
ax.set_ylabel('Intercept, nN')
plt.xlim([-5000, 0])
plt.ylim([0, 4])
cbar = plt.colorbar(sc)
cbar.ax.set_ylabel('Dipole moment, Debye')
plt.tight_layout()
plt.savefig('interaction-energy-nohbond-all-dipole.pdf')
