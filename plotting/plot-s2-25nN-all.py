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
    s2 = []
    s2_err = []
    for chainlength in chainlengths:
        s2_values = df[(df.chainlength==chainlength) &
                       (df.terminal_group==terminal_group)].S2.values
        s2.append(np.mean([val['25nN'] for val in s2_values]))
        s2_err.append(np.std([val['25nN'] for val in s2_values]))
    if i < int(n_groups/2):
        ax1.errorbar(chainlengths, s2, yerr=s2_err, marker='o',
                     label=terminal_group)
    else:
        ax2.errorbar(chainlengths, s2, yerr=s2_err, marker='o',
                     label=terminal_group)

plt.xlabel('Chain length, # of carbons')
ax1.set_ylabel('Nematic order (S2)')
ax1.set_xticks(np.linspace(5,17,5))
ax2.set_xticks(np.linspace(5,17,5))
#ax1.legend()
#ax2.legend()
fig.set_size_inches(14,6)
plt.tight_layout()
plt.savefig('s2.pdf')
