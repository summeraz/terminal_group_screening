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
ax1 = plt.subplot(121)
ax2 = plt.subplot(122, sharey=ax1)
plt.setp(ax2.get_yticklabels(), visible=False)

for i, terminal_group in enumerate(terminal_groups):
    tilt = []
    tilt_err = []
    for chainlength in chainlengths:
        tilt_values = df[(df.chainlength==chainlength) &
                        (df.terminal_group==terminal_group)].tilt.values
        tilt.append(np.mean([val['25nN'] for val in tilt_values]))
        tilt_err.append(np.std([val['25nN'] for val in tilt_values]))
    if i < int(n_groups/2):
        ax1.errorbar(chainlengths, tilt, yerr=tilt_err, marker='o',
                     label=terminal_group)
    else:
        ax2.errorbar(chainlengths, tilt, yerr=tilt_err, marker='o',
                     label=terminal_group)

plt.xlabel('Chain length, # of carbons')
ax1.set_ylabel('Avg. tilt angle, degrees')
ax1.set_xticks(np.linspace(5,17,5))
ax2.set_xticks(np.linspace(5,17,5))
#ax1.legend()
#ax2.legend()
fig.set_size_inches(14,6)
plt.tight_layout()
plt.savefig('tilt.pdf')
