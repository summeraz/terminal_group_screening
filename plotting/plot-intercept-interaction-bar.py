import matplotlib.pyplot as plt
import matplotlib.ticker
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

intercept = np.array([df[(df.chainlength==17) &
                         (df.terminal_group==terminal_group)].intercept.mean()
                      for terminal_group in terminal_groups])
energy = np.array([df[(df.chainlength==17) &
                      (df.terminal_group==terminal_group)].shear_5nN_Etotal
                   for terminal_group in terminal_groups])
energy_mean = np.mean(energy, axis=1)[:,0]
energy_err = np.array([np.std(tg[:,0]) for tg in energy])
intercept_err = np.array([df[(df.chainlength==17) &
                             (df.terminal_group==terminal_group)].intercept.std()
                          for terminal_group in terminal_groups])

inds = intercept.argsort()
intercept = intercept[inds]
energy = energy_mean[inds]
intercept_err = intercept_err[inds]
energy_err = energy_err[inds]
terminal_groups = terminal_groups[inds]

plt.yticks(np.arange(n_groups)+0.15, tuple(terminal_groups), ha='right')
ax2 = ax.twiny()
height = 0.35

ax.barh(np.arange(n_groups), intercept, height=height, xerr=intercept_err,
        align='center', color='#1f77b4')
ax2.barh(np.arange(n_groups) + height, energy, height=height, xerr=energy_err,
        align='center', color='#ff7f0e')

ax.set_xlabel('Intercept, nN', color='#1f77b4')
ax2.set_xlabel('Interaction energy, kJ/mol', color='#ff7f0e', labelpad=10)
ax2.invert_xaxis()

nticks = 6
ax.xaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
ax2.xaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
ax.set_xticks([round(tick, 2) for tick in ax.get_xticks()])
ax2.set_xticks([round(tick, 0) for tick in ax2.get_xticks()])

fig.set_size_inches(16,10)
plt.tight_layout()
plt.savefig('intercept-interaction-c17-bar.pdf')
