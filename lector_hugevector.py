# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 17:39:17 2020

@author: admin
"""

import numpy as np
from matplotlib import pyplot as plt

archivo='3.5hs_pcor_celulas6 hugevector'
#archivo='simulacion 20200625 3 hugevector'

#==============================================================================
# Con este programa leemos el hugevector y lo transformamos en una gran matriz
# donde cada submatriz es una imagen.
#==============================================================================
def Matriz_hugevector(Archivo, Size,Frames):
    Vector= open(Archivo)
    Linea=Vector.readline()
    Frame_posicion_inicial=int(int(Linea[0:9])%Size**2)
    Frame_numero_inicial=int(np.floor(int(Linea[0:9])/Size**2))  
    if Frame_posicion_inicial!=0: #esto es un control para que siempre inicie en la posicion 0
        j=0
        while j<Size**2-Frame_posicion_inicial:
            Linea=Vector.readline()
            j=j+1
    Gran_matriz=[]
    for j in range(Frames-Frame_numero_inicial):
        Matriz=np.empty([Size,Size])
        for i in range(Size**2):
            Fra=int(int(Linea[0:9])%Size**2)
            Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]=Matriz[Size-1-int(np.floor(Fra/Size)),int(Fra%Size)]+int(Linea[9:17])
            Linea=Vector.readline()
        Gran_matriz.append(Matriz)
    return np.array(Gran_matriz)

#==============================================================================
# Este programa permite guardar la gran matriz en un txt, se puede guardar como
# un unico vector o como una matriz donde cada columna es una imagen.
#==============================================================================
def Guardo_granmatriz(Gran_matriz,Nombre,Tipo='Matriz'): 
    if Tipo == 'Vector':
        np.savetxt('%s.txt' %archivo, np.reshape(simulacion,len(simulacion)*len(simulacion[0])**2),delimiter=',')
    if Tipo == 'Matriz':
        np.savetxt('%s matriz.txt' %archivo, np.reshape(simulacion,(len(simulacion),len(simulacion[0])**2)),delimiter=',')
    else:
        print('Especifique como guardar: Matriz o Vector')
        
        
size=128
frame=2000
simulacion=Matriz_hugevector(Archivo=archivo, Size=size,Frames=frame) 
        
        