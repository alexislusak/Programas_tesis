# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:45:58 2020

@author: admin
"""


import FCS
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def pCF_linea(Matriz,R0,R1,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0):
    Frames=len(Matriz[:,0,0])
    Size=len(Matriz[0,:,0])    
    P0=Matriz[:,R0,0]
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size**2+Tiempo_retorno_linea
    G=FCS.corrlineal_fft(P0,Matriz[:,R1,0])
    Tiempo_retrazo=(R1-R0)*Tiempo_pixel
    Tau=np.linspace(0,int(Frames/2)-1,int(Frames/2))*Tiempo_imagen+Tiempo_retrazo
    return np.array(G),np.array(Tau)  

def pCF_lineas(Matriz,PCF,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0):
    Size=len(Matriz[0,:,0])
    Lineas=[]
    for i in range(Size):
        Lineas.append(pCF_linea(Matriz=Matriz,R0=i,R1=i+PCF,Tiempo_pixel=Tiempo_pixel,Tiempo_retorno_linea=Tiempo_retorno_linea,Tiempo_imagen=Tiempo_imagen))
    return np.array(Lineas)


Archivo=r'C:\Users\admin\Desktop\Line Scan difusion isotropica 2D sin barreras tp_1us - 100 ciclos1.b64'
Matriz=FCS.read_B64(Archivo,Size=256,Voltear=False,Line=True)        
Tiempo_pixel=10**(-6)
PCF=0


lineas=pCF_lineas(Matriz=Matriz,PCF=PCF,Tiempo_pixel=Tiempo_pixel)       

        
movil=3
especial=True

fig = plt.figure('Alfombra')
ax = Axes3D(fig)
plt.ion()
for i in range(len(lineas[:,0,0])):
    if movil ==0:
        X =np.ones(len(lineas[i,1,:]))*i
        if PCF==0:
            Y =np.log10(lineas[i,1,:])
        else:
            Y =-np.log10(Tiempo_pixel*PCF) + np.log10(lineas[i,1,:])
        Z = np.array(lineas[i,0,:])
    else:
        if PCF==0:
            Y =np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
        else:
            Y =-np.log10(Tiempo_pixel*PCF) + np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
        Z = np.array(FCS.moving_average(lineas[i,0,:], n=movil,Especial=especial))
        X =np.ones(len(Z))*i
    ax.plot(X, Y, Z)
    ax.set_xlabel('Posición')
    ax.set_ylabel('Tiempo de correlación (s)')
    ax.set_zlabel('Correlación')
    ax.set_title('PCF distance=%s' %(PCF),loc='right')
    ax.set_zlim(-0.2,4)
plt.savefig(Archivo +' pcf %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
plt.show()
plt.close()      



  