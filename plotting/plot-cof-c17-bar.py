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

cof = np.array([df[(df.chainlength==17) &
                   (df.terminal_group==terminal_group)].COF.mean()
                for terminal_group in terminal_groups])
cof_err = np.array([df[(df.chainlength==17) &
                       (df.terminal_group==terminal_group)].COF.std()
                    for terminal_group in terminal_groups])

# Sort by COF
inds = cof.argsort()
cof = cof[inds]
cof_err = cof_err[inds]
terminal_groups = terminal_groups[inds]

ax.barh(np.arange(n_groups), cof, height=0.5, xerr=cof_err, align='center')
plt.yticks(np.arange(n_groups)+0.15, tuple(terminal_groups), ha='right')

ax.set_xlabel('Coefficient of friction')
ax.set_xlim(0.08, 0.20)
fig.set_size_inches(16,10)
plt.tight_layout()
plt.savefig('cof-c17-bar.pdf')
