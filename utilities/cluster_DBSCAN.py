import numpy as np
from sklearn.cluster import DBSCAN as DBSCAN
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

data = np.loadtxt("../data/order_v.csv", delimiter=",")
data = data[:10000, 1:]
clustering = DBSCAN(eps=3, min_samples=2).fit(data)
labels = clustering.labels_

df = pd.DataFrame({
    'X': data[:, 0],
    'Y': data[:, 1],
    'label': labels
})

fg = sns.FacetGrid(data=df, hue='label')
fg.map(plt.scatter, 'X', 'Y').add_legend()
plt.show()