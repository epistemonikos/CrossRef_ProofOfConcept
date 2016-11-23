__author__ = 'fmosso'

import csv
from collections import defaultdict
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

columns = defaultdict(list)
with open('rankingResults140k.tsv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v)# append the value into the appropriate list
                                 # based on column name k
header = []
with open('rankingResults140k.tsv') as f:
    reader = csv.DictReader(f)
    header = f.readline().split(',')
header[(len(header)-1)] = header[(len(header)-1)][:-1] #remove the breakline


CUANTITIESRANGES ={'green': 0, 'yellow' : 0, 'red':0, 'black':0 }

def getCuentitiesRanges(l,r1,r2):
    cuantitiesWeight = CUANTITIESRANGES.copy()
    for weight in l:
        fw = float(weight)
        if fw >= r1:
            cuantitiesWeight['green'] +=1
        if fw < r1 and fw >= r2:
            cuantitiesWeight['yellow'] +=1
        if fw < r2 and fw > 0:
            cuantitiesWeight['red'] +=1
        else:
            cuantitiesWeight['black'] +=1
    return  cuantitiesWeight


results = {}
for key, val in columns.items():
    results[key] = getCuentitiesRanges(val,0.95,0.8)



N = 5

Green = []
Yellow = []
Red = []

for head in header:
    Green.append(results[head]['green'])
    Yellow.append(results[head]['yellow'])
    Red.append(results[head]['red'])

ind = np.arange(N)  # the x locations for the groups
width = 0.25       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, Green, width, color='g')

rects2 = ax.bar(ind + width, Yellow, width, color='y')

rects3 = ax.bar(ind + 2*width, Red, width, color='r')

# add some text for labels, title and axes ticks
ax.set_ylabel('Cantidad')
ax.set_title('Cantidad de referencias según distintos rankings, muestra = 140k')
ax.set_xticks(ind + 1.5*width)
ax.set_xticklabels(header)

ax.legend((rects1[0], rects2[0],rects3[0]), ('Mayor o igual a 0.95', 'Entre 0.95 y 0.8','Menor a 0.8'))


plt.show()