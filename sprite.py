# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:00:09 2020

@author: admin
"""

import FCS
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

#==============================================================================
# Este programa calcula los XY para que se este a una distancia R de un punto.
#============================================================================== 
def puntos_correlacion(R):
    X=[]
    Y=[]
    y=R
    while y >= 0:
        x=0
        if (x**2+y**2)**0.5<=R-1:
            while (x**2+y**2)**0.5<=R+0.5:
                x=x+1
            x=x-1
        Y.append(y)
        X.append(x)
        if y==0:
            Y.append(y)
            X.append(-x)
        if x==0:
            Y.append(-y)
            X.append(x)
        if y!=0 and x!=0:
            Y.append(y)
            Y.append(-y)
            Y.append(-y)
            X.append(-x)
            X.append(-x)
            X.append(x)
        while (y**2 + (x+1)**2)**0.5<=R+0.5:
            x=x+1
            Y.append(y)
            X.append(x)
            if y==0:
                Y.append(y)
                X.append(-x)
            if y!=0 and x!=0:
                Y.append(y)
                Y.append(-y)
                Y.append(-y)
                X.append(-x)
                X.append(-x)
                X.append(x)
        y=y-1
    return X,Y

#==============================================================================
# Calcula el esprite para el vector R1 posiciones a distancia R
#==============================================================================
def sprite(Matriz,R0,R1):
    P0=Matriz[:,R0[0],R0[1]]
    G=[]
    for i in range(len(R1[0])):
        G.append(FCS.corrlineal_fft(P0,Matriz[:,R1[0][i],R1[1][i]]))
    return np.array(G)
              
#==============================================================================
# Calcula los tiempos para el sprite
#==============================================================================        
def tau(R1,Frames,Size,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_retorno_final=0,Tiempo_imagen=0):
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size**2+Tiempo_retorno_linea*Size+Tiempo_retorno_final
    Tau=[]
    for i in range(len(R1[0])):
        Tiempo_retrazo=(R1[0][i])*Tiempo_pixel+(R1[1][i])*(Tiempo_retorno_linea+Size*Tiempo_pixel)
        Tau.append(np.linspace(0,Frames-1,Frames)*Tiempo_imagen+Tiempo_retrazo)
    return np.array(Tau)



#==============================================================================
# Abro el archivo y grafico.
#==============================================================================
Archivo=r'C:\Users\admin\Desktop\simulacion 20200526 1.b64'
pCF_distance=2
r0=np.array([10,10])
x1,y1=np.array(puntos_correlacion(pCF_distance))
Matriz=FCS.read_B64(Archivo)
Frames=len(Matriz)
Size=len(Matriz[0])
Tiempo_pixel=10**(-6)

spri=sprite(Matriz=Matriz,R0=r0,R1=np.array([r0[0]+x1,r0[1]+y1]))
taus=tau(R1=[x1,y1],Frames=len(spri[0]),Size=Size,Tiempo_pixel=Tiempo_pixel)

# ah=spri[0][:100]
# fig = plt.figure()
# ax = Axes3D(fig)
# X = np.array([np.linspace(0, 40, len(ah))])
# Y = np.array([np.linspace(0, 0, len(ah))])
# X, Y = np.meshgrid(X, Y)
# Z = np.array([ah])
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
# plt.show()


fig = plt.figure()
ax = Axes3D(fig)
plt.ion()
for i in range(len(spri)):
    X =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[0]))*x1[i]
    Y =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[0]))*y1[i]
    # X =(taus[0])*x1[i]
    # Y =(taus[0])*y1[i]
    # X, Y = np.meshgrid(X, Y)
    Z = np.array(spri[0])
    ax.plot(X, Y, Z)
plt.show()

# from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


