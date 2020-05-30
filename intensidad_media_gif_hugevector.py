# -*- coding: utf-8 -*-
"""
Created on Mon May 25 02:38:23 2020

@author: admin
"""

import numpy as np
from matplotlib import pyplot as plt

hugevector= open('simulacion 20200523 1 hugevector')

def creo_matriz(Vector, Size,Frames,Average=0):
    Matriz=np.zeros([Size,Size])
    for i in range(Frames*Size**2):
        Linea=Vector.readline()
        Fra=int(int(Linea[0:9])%Size**2)
        Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]=Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]+int(Linea[9:17])
    return Matriz

matriz=creo_matriz(hugevector, Size=256,Frames=400)
plt.figure('intensidad')
plt.pcolor(matriz)

