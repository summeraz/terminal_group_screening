import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams["font.weight"] = "demibold"
plt.rc('axes.spines', top=False, right=False)
sns.set(font_scale=3)
sns.set_style("ticks", {"xtick.major.size" : 8, "ytick.major.size" : 8})

variables = ['Molecular weight', 'Dipole moment', 'Chain length', 'COF', 'Intercept',
             'Nematic order', 'Tilt angle', 'Δ Tilt angle',
             'Interdigitation', 'Δ Interdigitation',
             'Interaction energy']
correlation_matrix = np.load('correlation-matrix-nohbond-poster-new.npy')
for i, row in enumerate(correlation_matrix):
    for j, val in enumerate(row):
        correlation_matrix[i][j] = round(val, 2)
        if abs(val) < 0.005:
            correlation_matrix[i][j] == 0.0

fig, ax = plt.subplots(figsize=(18,18))
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=True, cmap='coolwarm', vmin=-1.0, vmax=1.0, center=0.0,
                 square=True, annot_kws={'size': 16, 'weight': 'semibold'},
                 cbar_kws={'ticks': [-1, -0.5, 0, 0.5, 1], 'shrink': 0.68,
                 'label': 'Pearson correlation coefficient'})
ax.tick_params(reset=True)
ax.xaxis.tick_top()
ax.tick_params(labelsize=24, direction='out')
plt.xticks(rotation=45, ha='left')
plt.tight_layout()
plt.savefig('correlation-heatmap-nohbond-poster-new.pdf')
