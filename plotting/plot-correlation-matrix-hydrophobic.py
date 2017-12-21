import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(font_scale=2)

variables = ['Molecular weight', 'Surface area', 'Dipole moment', 'Chain length',
             'Solvation energy', 'Solvation energy (polar)',
             'Solvation energy (nonpolar)', 'Enthalpy (vibrational)',
             'Entropy (translational)', 'Entropy (rotational)',
             'Entropy (vibrational)', 'Heat capacity (vibrational)', 'COF',
             'Intercept', 'Nematic order', 'Tilt angle', 'Interdigitation',
             'Δ Interdigitation', 'Interaction energy']
correlation_matrix = np.load('correlation-matrix-hydrophobic.npy')

fig, ax = plt.subplots(figsize=(18,18))
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=True, cmap='coolwarm', vmin=-1.0, vmax=1.0, center=0.0,
                 square=True, annot_kws={'size': 11, 'weight': 'semibold'},
                 cbar_kws={'ticks': [-1, -0.5, 0, 0.5, 1], 'shrink': 0.74})
ax.tick_params(labelsize=16)
plt.xticks(rotation=-45, ha='left')
plt.tight_layout()
plt.savefig('correlation-hydrophobic-heatmap.pdf')
