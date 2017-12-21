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

fig = plt.figure(1)
ax = plt.subplot(111)

cofs = []
intercepts = []
for job in project:
    cof = job.document['COF']
    intercept = job.document['intercept']
    if cof < 0.05:
        print(job.ws)
    cofs.append(job.document['COF'])
    intercepts.append(job.document['intercept'])
ax.scatter(cofs, intercepts, color='black', marker='o', s=75)

plt.xlabel('Coefficient of friction')
ax.set_ylabel('Intercept, nN')
plt.xlim([-0.05, 0.5])
plt.ylim([-20.0, 20.0])
plt.tight_layout()
plt.savefig('cof-intercept-all.pdf')
