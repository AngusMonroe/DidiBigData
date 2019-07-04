from matplotlib import pyplot as plt
import json

with open('../data/order2turnNum.json', 'r', encoding='utf-8') as json_file:
    order2ratio = json.load(json_file)

data = []
for order in order2ratio.keys():
    data.append(order2ratio[order])

plt.hist(data, bins=20, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.show()