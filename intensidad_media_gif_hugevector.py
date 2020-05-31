# -*- coding: utf-8 -*-
"""
Created on Mon May 25 02:38:23 2020

@author: admin
"""

import numpy as np
from matplotlib import pyplot as plt

archivo='3.5hs_pcor_celulas6 hugevector'
hugevector= open(archivo)

def creo_matriz(Vector, Size,Frames):
    Matriz=np.zeros([Size,Size])
    for i in range(Frames*Size**2):
        Linea=Vector.readline()
        Fra=int(int(Linea[0:9])%Size**2)
        Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]=Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]+int(Linea[9:17])
    return Matriz

def guardo_matriz(Vector,Size,Frames,Average,Name):
    plt.ioff()
    for j in range(int(np.floor(Frames/Average))):
        Matriz=np.zeros([Size,Size])
        for i in range(Average*Size**2):
            Linea=Vector.readline()
            Fra=int(int(Linea[0:9])%Size**2)
            Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]=Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]+int(Linea[9:17])
        plt.pcolor(Matriz)
        plt.savefig(fname='%s %s.png'%(Name,j),dpi=150)
        plt.close()
    return


#matriz=creo_matriz(hugevector, Size=256,Frames=40)
#plt.figure('intensidad')
#plt.pcolor(matriz)
    
guardo_matriz(Vector=hugevector,Size=128,Frames=8093,Average=202,Name=archivo)

