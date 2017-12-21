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

hbonding_groups = ['amino', 'carboxyl', 'hydroxyl']

variables = ['Molecular weight', 'Dipole moment', 'Chain length', 'COF', 'Intercept',
             'Nematic order', 'Tilt angle', 'Δ(5nN->25nN) Tilt angle',
             'Interdigitation', 'Δ(5nN->25nN) Interdigitation', 'Roughness',
             'Interaction energy']

data = [[] for _ in variables]

for job in project.find_jobs():
    if job.sp['terminal_group'] not in hbonding_groups:
        for i, var in enumerate(variables):
            if var == 'Chain length':
                val = job.sp['chainlength']
            elif var == 'COF':
                val = job.document['COF']
            elif var == 'Intercept':
                val = job.document['intercept']
            elif var == 'Tilt angle':
                val = job.document['tilt']['15nN']
            elif var == 'Δ(5nN->25nN) Tilt angle':
                val = job.document['tilt']['25nN'] - job.document['tilt']['5nN']
            elif var == 'Nematic order':
                val = job.document['S2']['15nN']
            elif var == 'Δ Nematic order':
                val = job.document['S2']['25nN'] - job.document['S2']['5nN']
            elif var == 'Interaction energy':
                val = job.document['shear_15nN_Etotal'][0]
            elif var == 'Δ Interaction energy':
                val = job.document['shear_25nN_Etotal'][0] - job.document['shear_5nN_Etotal'][0]
            elif var == 'Molecular weight':
                val = job.document['molecular_weight']
            elif var == 'Surface area':
                val = job.document['surface_area']
            elif var == 'Dipole moment':
                val = job.document['dipole_moment']
            elif var == 'Interdigitation':
                val = job.document['interdigitation']['15nN']
            elif var == 'Δ(5nN->25nN) Interdigitation':
                val = job.document['interdigitation']['25nN'] - job.document['interdigitation']['5nN']
            elif var == 'Roughness':
                val = job.document['roughness']['15nN']
            elif var == 'Δ Roughness':
                val = job.document['roughness']['25nN'] - job.document['roughness']['5nN']
            data[i].append(val)

correlation_matrix = np.empty([2, len(variables)])

for i, var1 in enumerate(['COF', 'Intercept']):
    for j, var2 in enumerate(variables):
        slope, intercept, r_val, p_val, err = stats.linregress(data[i], data[j])
        correlation_matrix[i, j] = r_val

np.save('correlation-matrix-cof-intercept-only', correlation_matrix)
