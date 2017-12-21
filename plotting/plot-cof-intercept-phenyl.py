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

markers = ['o', 's', '^', 'd', 'P']

for i, terminal_group in enumerate(terminal_groups):
    if terminal_group == 'phenyl':
        for j, chainlength in enumerate(chainlengths):
            cofs = []
            intercepts = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                cofs.append(job.document['COF'])
                intercepts.append(job.document['intercept'])
                ax.scatter(cofs, intercepts, color='green',
                           marker=markers[j], s=150)
    if terminal_group == 'nitrophenyl':
        for j, chainlength in enumerate(chainlengths):
            cofs = []
            intercepts = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                cofs.append(job.document['COF'])
                intercepts.append(job.document['intercept'])
                ax.scatter(cofs, intercepts, color='blue',
                           marker=markers[j], s=150)
    if terminal_group == 'fluorophenyl':
        for j, chainlength in enumerate(chainlengths):
            cofs = []
            intercepts = []
            for job in project.find_jobs({'terminal_group': terminal_group,
                                          'chainlength': chainlength}):
                cofs.append(job.document['COF'])
                intercepts.append(job.document['intercept'])
                ax.scatter(cofs, intercepts, color='pink',
                           marker=markers[j], s=150)

plt.xlabel('Coefficient of friction')
ax.set_ylabel('Intercept, nN')
#plt.xlim([0.08, 0.22])
#plt.ylim([0, 4.5])
plt.tight_layout()
plt.savefig('cof-intercept-phenyl.pdf')
