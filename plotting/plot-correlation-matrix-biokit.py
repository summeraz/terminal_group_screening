import matplotlib.pyplot as plt
import numpy as np
from biokit.viz import corrplot

plt.rcParams["font.weight"] = "demibold"
plt.rc('axes.spines', top=False, right=False)
'''
sns.set(font_scale=3)
sns.set_style("ticks", {"xtick.major.size" : 8, "ytick.major.size" : 8})
'''

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

fig, ax = plt.subplots(figsize=(16, 12))
'''
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=True, cmap='coolwarm', vmin=-1.0, vmax=1.0, center=0.0,
                 square=True, annot_kws={'size': 16, 'weight': 'semibold'},
                 cbar_kws={'ticks': [-1, -0.5, 0, 0.5, 1], 'shrink': 0.68,
                 'label': 'Pearson correlation coefficient'})
'''
c = corrplot.Corrplot(correlation_matrix)
c.order(inplace=True)
c.plot(fig=fig, grid=True, rotation=30, upper='circle', lower=None, shrink=0.9,
       facecolor='white', colorbar=True, label_color='black', fontsize='large',
       edgecolor='black', method='circle', cmap='coolwarm', ax=ax)

#ax.tick_params(reset=True)
#ax.xaxis.tick_top()
#ax.tick_params(labelsize=24, direction='out')
#plt.xticks(rotation=45, ha='left')
plt.tight_layout()
plt.savefig('correlation-heatmap-biokit.pdf')
