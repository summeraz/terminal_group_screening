import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats
import seaborn as sns

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)

variables = ['Molecular weight', 'Chain length', 'COF', 'Intercept', 'Nematic order',
             'Tilt angle', 'Interaction energy']

data = [[] for _ in variables]

for job in project.find_jobs():
    for i, var in enumerate(variables):
        if var == 'Chain length':
            val = job.sp['chainlength']
        elif var == 'COF':
            val = job.document['COF']
        elif var == 'Intercept':
            val = job.document['intercept']
        elif var == 'Tilt angle':
            val = job.document['tilt']['15nN']
        elif var == 'Nematic order':
            val = job.document['S2']['15nN']
        elif var == 'Interaction energy':
            val = job.document['shear_15nN_Etotal'][0]
        elif var == 'Molecular weight':
            val = job.document['molecular_weight']
        data[i].append(val)

correlation_matrix = np.empty([len(variables), len(variables)])

for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        slope, intercept, r_val, p_val, err = stats.linregress(data[i], data[j])
        correlation_matrix[i, j] = r_val

np.save('correlation-matrix', correlation_matrix)
