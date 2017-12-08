#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:32:02 2017

@author: zhangchi
"""

# bar draw for showing algorithm comparison results

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


sns.set(style="dark")

N = 5
M = 3

ind = np.arange(N)  # the x locations for the groups
width = 1./(M+1)     # the width of the bars

fig, ax = plt.subplots()
fig.set_size_inches(7, 5.5)

men_means = (20, 35, 20, 35, 27)
rects1 = ax.bar(ind, men_means, width, color="white", edgecolor = "black", linewidth=2)#, color='r')#, yerr=men_std)
ax.bar(ind, (18, 33, 25, 33, 26), width*0.7)#, alpha=0.5)
ax.bar(ind, (14, 33, 28, 33, 26), width*0.3, color ='black')#, alpha=0.5)

women_means = (25, 32, 34, 20, 25)
rects2 = ax.bar(ind + width, women_means, width)#, color='y')#, yerr=women_std)

mi_means = (15, 31, 35, 21, 24)
rects3 = ax.bar(ind + width * 2, mi_means, width)

# add some text for labels, title and axes ticks
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

ax.legend((rects1[0], rects2[0], rects3[0]), ('Men', 'Women','Mi'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.show()

# =============================================================================
# import matplotlib.pyplot as plt
# from matplotlib.patches import Ellipse, Polygon
# import seaborn as sns
# 
# sns.set()
# 
# fig = plt.figure()
# ax1 = fig.add_subplot(131)
# ax1.bar(range(1, 5), range(1, 5), edgecolor='black')
# ax1.bar(range(1, 5), [3,-1,2,1], bottom=range(1, 5),
#         edgecolor='black')
# ax1.set_xticks([1.5, 2.5, 3.5, 4.5])
# 
# plt.show()
# =============================================================================

# =============================================================================
# import numpy as np
# import matplotlib.pyplot as plt
# 
# 
# N = 5
# menMeans = (20, 35, 30, 35, 27)
# womenMeans = (25, 32, 34, 20, 25)
# menStd = (2, 3, 4, 1, 2)
# womenStd = (3, 5, 2, 3, 3)
# ind = np.arange(N)    # the x locations for the groups
# width = 0.35       # the width of the bars: can also be len(x) sequence
# 
# p1 = plt.bar(ind, menMeans, width, yerr=menStd)
# p2 = plt.bar(ind, womenMeans, width,
#              bottom=menMeans, yerr=womenStd)
# 
# plt.ylabel('Scores')
# plt.title('Scores by group and gender')
# plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
# plt.yticks(np.arange(0, 81, 10))
# plt.legend((p1[0], p2[0]), ('Men', 'Women'))
# 
# plt.show()
# =============================================================================
