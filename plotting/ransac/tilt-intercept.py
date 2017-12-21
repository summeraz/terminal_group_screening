import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats
from sklearn import linear_model, datasets
from tabulate import tabulate

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)
chainlengths = df.chainlength.unique()
chainlengths.sort()
terminal_groups = df.terminal_group.unique()
terminal_groups.sort()
n_groups = len(terminal_groups)

fig = plt.figure(1)
ax = plt.subplot(111)

all_x = []
all_y = []
all_terminal_groups = []
all_chainlengths = []

for i, terminal_group in enumerate(terminal_groups):
    for j, chainlength in enumerate(chainlengths):
        x_local = []
        y_local = []
        for job in project.find_jobs({'terminal_group': terminal_group,
                                      'chainlength': chainlength}):
            x_local.append(job.document['tilt']['15nN'])
            y_local.append(job.document['intercept'])
        all_x.append(np.mean(x_local))
        all_y.append(np.mean(y_local))
        all_terminal_groups.append(terminal_group)
        all_chainlengths.append(chainlength)

all_x = np.array(all_x)
all_y = np.array(all_y)
X = np.array([[val] for val in all_x])
lr = linear_model.LinearRegression()
lr.fit(X, all_y)
_, _, r_all, _, _ = stats.linregress(all_x, all_y)

ransac = linear_model.RANSACRegressor(random_state=92)
ransac.fit(X, all_y)
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

outliers = np.array([[all_terminal_groups[i], all_chainlengths[i]] for i, val
    in enumerate(outlier_mask) if val])
headers = ['Terminal group', 'Chain Length']
table = tabulate(outliers, headers, tablefmt='fancy_grid')
print(table)

_, _, r_ransac, _, _ = stats.linregress(all_x[inlier_mask], all_y[inlier_mask])

line_X = np.linspace(all_x.min(), all_x.max(), 10)[:, np.newaxis]
line_y = lr.predict(line_X)
line_y_ransac = ransac.predict(line_X)

print("Pearson correlations (Linear regression, RANSAC):")
print(r_all, r_ransac)

plt.scatter(X[inlier_mask], all_y[inlier_mask], color='yellowgreen', marker='.',
    s=150)
plt.scatter(X[outlier_mask], all_y[outlier_mask], color='red', marker='.', s=150)
plt.plot(line_X, line_y, color='navy', label='LR ({:.3f})'.format(r_all))
plt.plot(line_X, line_y_ransac, color='cornflowerblue', 
    label='RANSAC ({:.3f})'.format(r_ransac))

plt.xlabel('Avg. tilt angle')
ax.set_ylabel('Intercept, nN')
plt.legend()
plt.tight_layout()
plt.savefig('tilt-intercept.pdf')
