import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

variables = ['Chainlength', 'COF', 'Intercept', 'Tilt-15nN', 'S2-15nN',
             'Energy-15nN']
correlation_matrix = np.load('correlation-matrix-hydrophilic.npy')

fig, ax = plt.subplots()
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=True)
plt.tight_layout()
plt.savefig('correlation-hydrophilic-heatmap.pdf')
