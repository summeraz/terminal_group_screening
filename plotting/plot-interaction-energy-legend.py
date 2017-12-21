import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac

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

for i, terminal_group in enumerate(terminal_groups):
    energies = []
    intercepts = []
    for job in project.find_jobs({'terminal_group': terminal_group}):
        interaction_energy = job.document['shear_5nN-Etotal']
        energies.append(interaction_energy[0])
        intercepts.append(job.document['intercept'])
    ax.scatter(np.mean(energies), np.mean(intercepts), color=colors[i],
               label=terminal_group, s=150)

plt.xlabel('Interaction energy, kJ/mol')
ax.set_ylabel('Intercept, nN')
ax.legend(ncol=1, fontsize=20)
plt.tight_layout()
plt.savefig('interaction-energy-legend.pdf')
