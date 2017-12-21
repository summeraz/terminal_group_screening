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
colors = hsv(np.linspace(0, 1.0, len(chainlengths)+2))
markers = ['o', 's', '^', 'd', 'P']

all_delta_interdigitations = []
all_cofs = []

for j, chainlength in enumerate(chainlengths):
    delta_interdigitations = []
    cofs = []
    for i, terminal_group in enumerate(terminal_groups):
        if terminal_group not in hbonding_groups:
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                delta_interdigitation = job.document['interdigitation']['25nN'] - \
                                        job.document['interdigitation']['5nN']
                delta_interdigitations.append(delta_interdigitation)
                all_delta_interdigitations.append(delta_interdigitation)
                cofs.append(job.document['COF'])
                all_cofs.append(job.document['COF'])
    ax.scatter(delta_interdigitations, cofs,
               color=colors[j], marker=markers[j], s=150)

    slope, intercept, r_val, p_val, err = stats.linregress(delta_interdigitations, cofs)
    xs = [-1000, 1000]
    ys = [slope*xval + intercept for xval in xs]
    ax.plot(xs, ys, marker='None', linestyle='--', color=colors[j],
            linewidth=2)
    print(chainlength, r_val, p_val)

plt.xlabel('Δ Interdigitation')
ax.set_ylabel('Coefficient of friction')
xrange = np.max(all_delta_interdigitations) - np.min(all_delta_interdigitations)
yrange = np.max(all_cofs) - np.min(all_cofs)
plt.xlim(np.min(all_delta_interdigitations) - xrange * 0.02, np.max(all_delta_interdigitations) + xrange * 0.02)
plt.ylim(np.min(all_cofs) - yrange * 0.02, np.max(all_cofs) + yrange * 0.02)
plt.tight_layout()
plt.savefig('cof-Dinterdigitation-chainlengths.pdf')
