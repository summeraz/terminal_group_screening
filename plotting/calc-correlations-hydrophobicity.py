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

hydrophobic_groups = ['acetyl', 'cyclopropyl', 'ethylene', 'fluorophenyl',
                      'isopropyl', 'methoxy', 'methyl', 'perfluoromethyl',
                      'phenyl']
hydrophilic_groups = ['amino', 'carboxyl', 'cyano', 'hydroxyl', 'nitro',
                      'nitrophenyl', 'pyrrole']

variables = ['Molecular weight', 'Surface area', 'Dipole moment', 'Chain length',
             'Solvation energy', 'Solvation energy (polar)',
             'Solvation energy (nonpolar)', 'Enthalpy (vibrational)',
             'Entropy (translational)', 'Entropy (rotational)',
             'Entropy (vibrational)', 'Heat capacity (vibrational)', 'COF',
             'Intercept', 'Nematic order', 'Tilt angle', 'Interdigitation',
             'Δ Interdigitation', 'Interaction energy']

data_hydrophobic = [[] for _ in variables]
data_hydrophilic = [[] for _ in variables]

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
        elif var == 'Surface area':
            val = job.document['surface_area']
        elif var == 'Dipole moment':
            val = job.document['dipole_moment']
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
        elif var == 'Interdigitation':
            val = job.document['interdigitation']['15nN']
        elif var == 'Δ Interdigitation':
            val = job.document['interdigitation']['25nN'] - job.document['interdigitation']['5nN']
        if job.sp['terminal_group'] in hydrophobic_groups:
            data_hydrophobic[i].append(val)
        else:
            data_hydrophilic[i].append(val)

correlation_matrix_hydrophobic = np.empty([len(variables), len(variables)])
correlation_matrix_hydrophilic = np.empty([len(variables), len(variables)])

for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        slope, intercept, r_val, p_val, err = stats.linregress(data_hydrophobic[i],
                                                               data_hydrophobic[j])
        correlation_matrix_hydrophobic[i, j] = r_val
        slope, intercept, r_val, p_val, err = stats.linregress(data_hydrophilic[i],
                                                               data_hydrophilic[j])
        correlation_matrix_hydrophilic[i, j] = r_val

np.save('correlation-matrix-hydrophobic', correlation_matrix_hydrophobic)
np.save('correlation-matrix-hydrophilic', correlation_matrix_hydrophilic)
