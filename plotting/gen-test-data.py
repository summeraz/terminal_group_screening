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

all_energies = []
all_intercepts = []
all_terminal_groups = []
all_chainlengths = []

for i, terminal_group in enumerate(terminal_groups):
    for j, chainlength in enumerate(chainlengths):
        energies = []
        intercepts = []
        for job in project.find_jobs({'terminal_group': terminal_group,
                                      'chainlength': chainlength}):
            interaction_energy = job.document['shear_5nN_Etotal']
            energies.append(interaction_energy[0])
            intercepts.append(job.document['intercept'])
        all_energies.append(np.mean(energies))
        all_intercepts.append(np.mean(intercepts))
        all_terminal_groups.append(terminal_group)
        all_chainlengths.append(chainlength)

np.savetxt('test-data-mean.txt', np.column_stack((all_energies, all_intercepts, all_terminal_groups, all_chainlengths)), fmt='%s')
