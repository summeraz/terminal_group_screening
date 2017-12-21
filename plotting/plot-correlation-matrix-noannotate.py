import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams["font.weight"] = "demibold"
plt.rc("axes.spines", top=False, right=False)
sns.set(font_scale=4)
sns.set_style("ticks", {"xtick.major.size" : 8, "ytick.major.size" : 8})

variables = ['Molecular weight', 'Surface area', 'Dipole moment', 'Chain length',
             'COF', 'Intercept', 'Nematic order', 'Δ Nematic order', 'Tilt angle',
             'Δ Tilt angle', 'Interdigitation', 'Δ Interdigitation', 'Roughness',
             'Δ Roughness', 'Interaction energy', 'Δ Interaction energy']
correlation_matrix = np.load('correlation-matrix.npy')

fig, ax = plt.subplots(figsize=(18,18))
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=False, cmap='coolwarm', vmin=-1.0, vmax=1.0, center=0.0,
                 square=True, annot_kws={'size': 11, 'weight': 'semibold'},
                 cbar_kws={'ticks': [-1, -0.5, 0, 0.5, 1], 'shrink': 0.6875,
                 'label': 'Pearson correlation coefficient'})

ax.tick_params(reset=True)
ax.tick_params(labelsize=20, direction='out')
plt.xticks(rotation=-45, ha='left')
plt.tight_layout()
plt.savefig('correlation-heatmap-noannotate.pdf')
