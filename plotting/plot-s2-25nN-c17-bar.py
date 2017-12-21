import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)
terminal_groups = df.terminal_group.unique()
terminal_groups.sort()
n_groups = len(terminal_groups)

fig, ax = plt.subplots()

s2 = []
s2_err = []
for terminal_group in terminal_groups:
    s2_values = df[(df.chainlength==17) &
                   (df.terminal_group==terminal_group)].S2.values
    s2.append(np.mean([val['25nN'] for val in s2_values]))
    s2_err.append(np.std([val['25nN'] for val in s2_values]))
s2 = np.asarray(s2)
s2_err = np.asarray(s2_err)

# Sort by COF
inds = s2.argsort()
s2 = s2[inds]
s2_err = s2_err[inds]
terminal_groups = terminal_groups[inds]

ax.bar(np.arange(n_groups), s2, width=0.5, yerr=s2_err, align='center')
plt.xticks(np.arange(n_groups)+0.15, tuple(terminal_groups), rotation=45, ha='right')

ax.set_ylabel('Nematic order')
ax.set_ylim(0.88,0.98)
fig.set_size_inches(16,10)
plt.tight_layout()
plt.savefig('s2-25nN-c17-bar.pdf')
