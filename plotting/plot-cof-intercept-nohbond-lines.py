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
colors = hsv(np.linspace(0, 1.0, len(chainlengths)+1))

for i, chainlength in enumerate(chainlengths):
    cl_cofs = []
    cl_intercepts = []
    for j, terminal_group in enumerate(terminal_groups):
        if terminal_group not in hbonding_groups:
            cofs = []
            intercepts = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                cofs.append(job.document['COF'])
                cl_cofs.append(job.document['COF'])
                intercepts.append(job.document['intercept'])
                cl_intercepts.append(job.document['intercept'])
            ax.scatter(np.mean(cofs), np.mean(intercepts), color='black',
                       marker='o', s=150)

    slope, intercept, r_val, p_val, err = stats.linregress(cl_cofs,
        cl_intercepts)
    xs = [0.09, 0.23]
    ys = [slope*xval + intercept for xval in xs]
    ax.plot(xs, ys, marker='None', linestyle='--', linewidth=2,
        label='C{}'.format(chainlength), color=colors[i])
    print(chainlength, r_val, p_val)

plt.xlabel('Coefficient of friction')
ax.set_ylabel('Intercept, nN')
plt.xlim([0.09, 0.23])
plt.ylim([0, 4])
plt.legend()
plt.tight_layout()
plt.savefig('cof-intercept-nohbond-lines.pdf')
