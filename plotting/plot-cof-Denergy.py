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

#hbonding_groups = ['amino', 'carboxyl', 'hydroxyl']
hbonding_groups = []

fig = plt.figure(1)
ax = plt.subplot(111)

hsv = plt.get_cmap('hsv')
colors = hsv(np.linspace(0, 1.0, len(terminal_groups)+1))
markers = ['o', 's', '^', 'd', 'P']

all_delta_interdigitations = []
all_cofs = []

for i, terminal_group in enumerate(terminal_groups):
    if terminal_group not in hbonding_groups:
        for j, chainlength in enumerate(chainlengths):
            delta_interdigitations = []
            cofs = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                delta_interdigitation = job.document['shear_25nN_Etotal'][0] - \
                                        job.document['shear_5nN_Etotal'][0]
                if delta_interdigitation > 0:
                    print(delta_interdigitation, terminal_group, chainlength)
                delta_interdigitations.append(delta_interdigitation)
                all_delta_interdigitations.append(delta_interdigitation)
                cofs.append(job.document['COF'])
                all_cofs.append(job.document['COF'])
            ax.scatter(delta_interdigitations, cofs,
                       color=colors[i], marker=markers[j], s=150)

slope, intercept, r_val, p_val, err = stats.linregress(all_delta_interdigitations,
    all_cofs)
xrange = np.max(all_delta_interdigitations) - np.min(all_delta_interdigitations)
xs = [np.min(all_delta_interdigitations) - xrange * 0.02, np.max(all_delta_interdigitations) + xrange * 0.02]
yrange = np.max(all_cofs) - np.min(all_cofs)
ys = [slope*xval + intercept for xval in xs]
ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
        linewidth=2)
print(r_val, p_val)

plt.xlabel('Δ Interaction energy')
ax.set_ylabel('Coefficient of friction')
plt.xlim(np.min(all_delta_interdigitations) - xrange * 0.02, np.max(all_delta_interdigitations) + xrange * 0.02)
plt.ylim(np.min(all_cofs) - yrange * 0.02, np.max(all_cofs) + yrange * 0.02)
plt.tight_layout()
plt.savefig('cof-Denergy.pdf')
