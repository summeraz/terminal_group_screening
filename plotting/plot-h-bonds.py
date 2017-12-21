import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac

h_bonding_groups = ['amino', 'carboxyl', 'hydroxyl']
loads = [5, 15, 25]

hsv = plt.get_cmap('hsv')
colors = hsv(np.linspace(0, 1.0, 4))
colors = dict(zip(h_bonding_groups, colors))

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)
chainlengths = df.chainlength.unique()
chainlengths.sort()

fig, ax = plt.subplots()

for terminal_group in h_bonding_groups:
    h_bonds_5 = []
    h_bonds_err_5 = []
    h_bonds_15 = []
    h_bonds_err_15 = []
    h_bonds_25 = []
    h_bonds_err_25 = []
    for chainlength in chainlengths:
        h_bonds_local_5 = []
        h_bonds_local_15 = []
        h_bonds_local_25 = []
        for job in project.find_jobs({'terminal_group': terminal_group,
                                      'chainlength': chainlength}):
            data_5 = np.loadtxt('{}/shear_5nN-h-bonds.txt'.format(job.ws))
            data_15 = np.loadtxt('{}/shear_15nN-h-bonds.txt'.format(job.ws))
            data_25 = np.loadtxt('{}/shear_25nN-h-bonds.txt'.format(job.ws))
            h_bonds_job_5 = np.mean(data_5[int(len(data_5)*0.6):,1])
            h_bonds_local_5.append(h_bonds_job_5)
            h_bonds_job_15 = np.mean(data_15[int(len(data_15)*0.6):,1])
            h_bonds_local_15.append(h_bonds_job_15)
            h_bonds_job_25 = np.mean(data_25[int(len(data_25)*0.6):,1])
            h_bonds_local_25.append(h_bonds_job_25)
        h_bonds_5.append(np.mean(h_bonds_local_5))
        h_bonds_err_5.append(np.std(h_bonds_local_5))
        h_bonds_15.append(np.mean(h_bonds_local_15))
        h_bonds_err_15.append(np.std(h_bonds_local_15))
        h_bonds_25.append(np.mean(h_bonds_local_25))
        h_bonds_err_25.append(np.std(h_bonds_local_25))
    if terminal_group == 'amino':
        ax.errorbar(chainlengths, h_bonds_5, yerr=h_bonds_err_5, label='5nN',
                    marker='o', color=colors[terminal_group], linestyle='-')
        ax.errorbar(chainlengths, h_bonds_15, yerr=h_bonds_err_15, label='15nN',
                    marker='s', color=colors[terminal_group], linestyle='dashed')
        ax.errorbar(chainlengths, h_bonds_25, yerr=h_bonds_err_25, label='25nN',
                    marker='^', color=colors[terminal_group], linestyle='dotted')
    else:
        ax.errorbar(chainlengths, h_bonds_5, yerr=h_bonds_err_5,
                    marker='o', color=colors[terminal_group], linestyle='-')
        ax.errorbar(chainlengths, h_bonds_15, yerr=h_bonds_err_15,
                    marker='s', color=colors[terminal_group], linestyle='dashed')
        ax.errorbar(chainlengths, h_bonds_25, yerr=h_bonds_err_25,
                    marker='^', color=colors[terminal_group], linestyle='dotted')

plt.xlabel('Chain length, # of carbons')
ax.set_ylabel('Hydrogen bonds')
ax.set_xticks(np.linspace(5,17,5))
ax.legend(ncol=1, loc='center right')
#fig.set_size_inches(16,8)
plt.tight_layout()
plt.savefig('h-bonds-load.pdf')
