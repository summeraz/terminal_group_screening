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

tilt = []
tilt_err = []
for terminal_group in terminal_groups:
    tilt_values = df[(df.chainlength==17) &
                   (df.terminal_group==terminal_group)].tilt.values
    tilt.append(np.mean([val['25nN'] for val in tilt_values]))
    tilt_err.append(np.std([val['25nN'] for val in tilt_values]))
tilt = np.asarray(tilt)
tilt_err = np.asarray(tilt_err)

# Sort by COF
inds = tilt.argsort()
tilt = tilt[inds]
tilt_err = tilt_err[inds]
terminal_groups = terminal_groups[inds]

ax.bar(np.arange(n_groups), tilt, width=0.5, yerr=tilt_err, align='center')
plt.xticks(np.arange(n_groups)+0.15, tuple(terminal_groups), rotation=45, ha='right')

ax.set_ylabel('Avg. tilt angle, degrees')
ax.set_ylim(35,43)
fig.set_size_inches(16,10)
plt.tight_layout()
plt.savefig('tilt-25nN-c17-bar.pdf')
