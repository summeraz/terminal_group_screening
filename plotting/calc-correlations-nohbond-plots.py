import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)

hbonding_groups = ['amino', 'carboxyl', 'hydroxyl']

variables = ['Molecular weight', 'Surface area', 'Dipole moment', 'Chain length',
             'COF', 'Intercept', 'Nematic order', 'Δ Nematic order', 'Tilt angle',
             'Δ Tilt angle', 'Interdigitation', 'Δ Interdigitation', 'Roughness',
             'Δ Roughness', 'Interaction energy', 'Δ Interaction energy']

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
            elif var == 'Interdigitation':
                val = job.document['interdigitation']['15nN']
            elif var == 'Δ Interdigitation':
                val = job.document['interdigitation']['25nN'] - job.document['interdigitation']['5nN']
            elif var == 'Roughness':
                val = job.document['roughness']['15nN']
            elif var == 'Δ Roughness':
                val = job.document['roughness']['25nN'] - job.document['roughness']['5nN']
            data[i].append(val)

for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        if i > j:
            fig = plt.figure(1)
            ax = plt.subplot(111)

            ax.scatter(data[i], data[j])
            slope, intercept, r_val, p_val, err = stats.linregress(data[i], data[j])
            xrange = np.max(data[i]) - np.min(data[i])
            yrange = np.max(data[j]) - np.min(data[j])
            xs = [np.min(data[i]) - xrange * 0.02, np.max(data[i]) + xrange * 0.02]
            ys = [slope*xval + intercept for xval in xs]
            ax.plot(xs, ys, marker='None', linestyle='--', color='black', alpha=0.95,
                    linewidth=2)

            plt.xlabel(var1)
            plt.ylabel(var2)
            plt.xlim(np.min(data[i]) - xrange * 0.02, np.max(data[i]) + xrange * 0.02)
            plt.ylim(np.min(data[j]) - yrange * 0.02, np.max(data[j]) + yrange * 0.02)
            plt.tight_layout()
            plt.savefig('correlation-{}-{}.pdf'.format(var1, var2))
            plt.clf()
