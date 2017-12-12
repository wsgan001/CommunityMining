#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:15:07 2017

@author: zhangchi
"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

F1ListSave = [[0.6348862405200446,
  0.7052845528455278,
  0.7413962635201582,
  0.757462686567165,
  0.7020905923344946,
  0.6988783433994838],
 [0.6367759498408286,
  0.7470447058729449,
  0.7738197114389869,
  0.7436960296009956,
  0.7389592211678601,
  0.7279812718495425],
 [0.6436473322810877,
  0.7173604586998481,
  0.7303728704679471,
  0.7065657709262303,
  0.7060532978675174,
  0.6792549581165334],
 [0.6101372953776756,
  0.7062096307661615,
  0.7002936812795872,
  0.6868062748403767,
  0.6742630350655315,
  0.6629856237175947],
 [0.5946120471995201,
  0.6670196047776317,
  0.6725138195606692,
  0.6675681611277327,
  0.6627145564359425,
  0.6542185581124403]]

F2ListSave = [[0.6567481402763009,
  0.7239999999999991,
  0.75654704170708,
  0.7716390423572743,
  0.7160068846815841,
  0.7127024722932651],
 [0.6540707378916631,
  0.756962011223936,
  0.7766831733069658,
  0.7469365334609377,
  0.7415313814285551,
  0.7312153308728948],
 [0.661443821860121,
  0.7257484346502489,
  0.7341230402328907,
  0.7094812637019373,
  0.7091652823835843,
  0.6827044841938368],
 [0.626400097019584,
  0.7129103521489638,
  0.7056264431180064,
  0.6901887711075834,
  0.6758807828365613,
  0.6660857051155549],
 [0.6102576483076032,
  0.6726400241961596,
  0.6766396486927061,
  0.6700603811857309,
  0.6655417710937245,
  0.6565592330966141]]

fig = plt.figure()
fig.set_size_inches(8, 5.5)
ax = fig.add_subplot(111)
ax.text(5.53, 0.731, u'No', fontsize=14)
#ax.text(5.5, 0.703, u'10%', fontsize=14)
ax.annotate('10%', xy=(4.5, 0.73), xytext=(3.6, 0.72), fontsize=14,
            arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=6))
ax.annotate('10%', xy=(4.85, 0.725), xytext=(3.6, 0.72), fontsize=14,
            arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=6))
ax.text(5.5, 0.688, u'20%', fontsize=14)
ax.text(5.5, 0.665, u'30%', fontsize=14)
ax.text(5.5, 0.655, u'40%', fontsize=14)

#ax.text(0.7, 0.53, u'Green lines stands for results run by uncertain R+K with Examination Phase', fontsize=14, color='green')
#ax.text(0.7, 0.515, u'Blue lines stands for uncertain run by R+K without Examination Phase', fontsize=14, color='blue')

ax.plot([1,2,3,4,5,6],F1ListSave[0],'go-',linewidth=1,label="uncertain R+K with Examination Phase")
ax.plot([1,2,3,4,5,6],F1ListSave[1],'go-',linewidth=1)
ax.plot([1,2,3,4,5,6],F1ListSave[2],'go-',linewidth=1)
ax.plot([1,2,3,4,5,6],F1ListSave[3],'go-',linewidth=1)
ax.plot([1,2,3,4,5,6],F1ListSave[4],'go-',linewidth=1)
#ax.plot([1],[1],'go-',linewidth=1,label="uncertain R+K with Examination Phase")

ax.plot([1,2,3,4,5,6],F2ListSave[0],'b<-',linewidth=1,label="uncertain R+K without Examination Phase")
ax.plot([1,2,3,4,5,6],F2ListSave[1],'b<-',linewidth=1)
ax.plot([1,2,3,4,5,6],F2ListSave[2],'b<-',linewidth=1)
ax.plot([1,2,3,4,5,6],F2ListSave[3],'b<-',linewidth=1)
ax.plot([1,2,3,4,5,6],F2ListSave[4],'b<-',linewidth=1)
#ax.plot([1],[1],'b<-',linewidth=1,label="uncertain R+K without Examination Phase")

ax.axis([0.5, 6.5, 0.58, 0.79])
plt.legend(prop={'size': 15})
plt.draw()