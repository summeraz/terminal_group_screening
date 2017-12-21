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

groups = ['amino', 'carboxyl', 'cyano', 'hydroxyl', 'nitro', 'nitrophenyl',
          'pyrrole']

variables = ['Molecular weight', 'Surface area', 'Dipole moment', 'Chain length',
             'COF', 'Intercept', 'Nematic order', 'Δ Nematic order', 'Tilt angle',
             'Δ Tilt angle', 'Interdigitation', 'Δ Interdigitation', 'Roughness',
             'Δ Roughness', 'Interaction energy', 'Δ Interaction energy']

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
        elif var == 'Δ Tilt angle':
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
            '''
            elif var == 'Solvation energy':
                val = job.document['total_solvation_energy']
            elif var == 'Solvation energy (polar)':
                val = job.document['polar_solvation_energy']
            elif var == 'Solvation energy (nonpolar)':
                val = job.document['nonpolar_solvation_energy']
            elif var == 'Enthalpy (vibrational)':
                val = job.document['enthalpy_vibrational']
            elif var == 'Entropy (translational)':
                val = job.document['entropy_translational']
            elif var == 'Entropy (rotational)':
                val = job.document['entropy_rotational']
            elif var == 'Entropy (vibrational)':
                val = job.document['entropy_vibrational']
            elif var == 'Heat capacity (vibrational)':
                val = job.document['heat_capacity_vibrational']
            '''
        elif var == 'Interdigitation':
            val = job.document['interdigitation']['15nN']
        elif var == 'Δ Interdigitation':
            val = job.document['interdigitation']['25nN'] - job.document['interdigitation']['5nN']
        elif var == 'Roughness':
            val = job.document['roughness']['15nN']
        elif var == 'Δ Roughness':
            val = job.document['roughness']['25nN'] - job.document['roughness']['5nN']
        if job.sp['terminal_group'] not in groups:
            data[i].append(val)

correlation_matrix = np.empty([len(variables), len(variables)])

for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        slope, intercept, r_val, p_val, err = stats.linregress(data[i], data[j])
        correlation_matrix[i, j] = r_val

np.save('correlation-matrix-nonpolar', correlation_matrix)
