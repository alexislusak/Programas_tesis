# -*- coding: utf-8 -*-
"""
Created on Tue May 19 23:35:45 2020

@author: admin
"""

import numpy as np
from matplotlib import pyplot as plt

anisotropia= np.loadtxt('4.5hs_pcor_celulas2_nucleo valores anisotropia',float)
direccion= np.loadtxt('4.5hs_pcor_celulas2_nucleo valores direccion',float)
intensidad= np.loadtxt('4.5hs_pcor_celulas2_nucleo valores intensidad',float)

#plt.hist(anisotropia,bins=253,range=[0.00321,0.82079])
#np.mean(anisotropia)
#np.std(anisotropia)


def quitoanisotropia0(Anisotropia, Direccion, Size=128, Size_automatico=True):
    if Size_automatico==True:
        Size=(len(Anisotropia))**0.5
    Anisotropia_corta=[]
    Direccion_corta=[]
    X=[]
    Y=[]
    for i in range(len(Anisotropia)):
        if Anisotropia[i]!=0.0:
            Direccion_corta.append(Direccion[i])
            Anisotropia_corta.append(Anisotropia[i])
            X.append(i%Size)
            Y.append(np.floor(i/Size))
    return [Anisotropia_corta, Direccion_corta, X, Y]

info=quitoanisotropia0(anisotropia, direccion)

def histogramas(Info):
    info=Info
    plt.figure('anisotropia')
    plt.hist(info[0],bins=255,label='%s +- %s' %(np.round(np.mean(info[0]),3),np.round(np.std(info[0]),3)))
    plt.legend()
    plt.figure('direcciones')
    plt.hist(info[1],bins=255,label='%s +- %s' %(np.round(np.mean(info[1]),3),np.round(np.std(info[1]),3)))
    plt.legend()

def creo_matriz(Vector, Size=128, Size_automatico=True):
    if Size_automatico==True:
        Size=int((len(Vector))**0.5)
        if (len(Vector))**0.5 - np.floor((len(Vector))**0.5)!=0:
            return print('El vector no es una matriz cuadrada')
    Matriz=np.zeros([Size,Size])
    for i in range(len(Vector)):
        Matriz[Size-1-int(np.floor(i/Size)),int(i%Size)]=Vector[i]
    return Matriz

matriz_anisotropia=creo_matriz(anisotropia)
matriz_direccion=creo_matriz(direccion)
plt.figure('anisotropia')
plt.pcolor(matriz_anisotropia,antialiaseds=False)
plt.figure('direccion')
plt.pcolor(matriz_direccion)


matriz_intensidad=creo_matriz(intensidad)
plt.figure('intensidad')
plt.pcolor(matriz_intensidad)

#se puede usar el reshape pero lo gira 180 grados
#prueba=anisotropia.reshape(126,126)
#plt.figure('anisotropia 2')
#plt.pcolor(prueba)
