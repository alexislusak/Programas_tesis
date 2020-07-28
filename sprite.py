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
def spriteseparada(Matriz,R0,R1):   
    P0=Matriz[:,R0[0],R0[1]]
    G=[]
    for i in range(len(R1[0])):
        G.append(FCS.corrlineal_fft(P0,Matriz[:,R1[0][i],R1[1][i]]))
    return np.array(G)

def sprite(Matriz,R0,R1,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_retorno_final=0,Tiempo_imagen=0):
    Frames=len(Matriz)
    Size=len(Matriz[0])    
    P0=Matriz[:,R0[0],R0[1]]
    G=[]
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size**2+Tiempo_retorno_linea*Size+Tiempo_retorno_final
    Tau=[]
    for i in range(len(R1[0])):
        G.append(FCS.corrlineal_fft(P0,Matriz[:,R1[0][i],R1[1][i]]))
        Tiempo_retrazo=(R1[0][i])*Tiempo_pixel+(R1[1][i])*(Tiempo_retorno_linea+Size*Tiempo_pixel)
        Tau.append(np.linspace(0,int(Frames/2)-1,int(Frames/2))*Tiempo_imagen+Tiempo_retrazo)
    return np.array(G),np.array(Tau)

def PCF(Matriz,R0,R1,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_retorno_final=0,Tiempo_imagen=0):
    Frames=len(Matriz)
    Size=len(Matriz[0])    
    P0=Matriz[:,R0[0],R0[1]]
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size**2+Tiempo_retorno_linea*Size+Tiempo_retorno_final
    G=FCS.corrlineal_fft(P0,Matriz[:,R1[0],R1[1]])
    Tiempo_retrazo=(R1[0])*Tiempo_pixel+(R1[1])*(Tiempo_retorno_linea+Size*Tiempo_pixel)
    Tau=np.linspace(0,int(Frames/2)-1,int(Frames/2))*Tiempo_imagen+Tiempo_retrazo
    return np.array(G),np.array(Tau)  
            
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

def moving_average(a, n=3,Especial=False) :
    if Especial==False:
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n
    if Especial==True:
        espacios= int(np.floor(np.log10(len(a))))
        ret= np.cumsum(a, dtype=float)
        ret0=ret
        ret0[n:] = ret0[n:] - ret0[:-n]
        ret0=ret0[n - 1:n+10-1] / n
        for i in range(espacios):
            ret1=np.cumsum(a, dtype=float)
            n0=n+10**(i+1)
            n1=n0+10**(i+2)
            if n1>len(a):
                n1=len(a)
            ret1[n0:]= ret1[n0:] - ret1[:-n0]
            ret1=ret1[n0 + int((10**(i+1)+10**(i))/2)-1:n1-1] / n0
            ret0=np.append(ret0,ret1)
        return ret0
    else:
        print('Especifique el modo Especial como True o False')
    

#==============================================================================
# Abro el archivo y grafico.
#==============================================================================
# Archivo0=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 11.b64'
# Archivo1=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 21.b64'
# Archivo2=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 31.b64'
# Archivo3=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 1.b64'
# Archivo4=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 2.b64'
# Archivo5=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 3.b64'
# Archivo6=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 4.b64'


# Archivos=[Archivo4]
# for Archivo in Archivos:
#     pCF_distances=[2,4,6,8]
#     for pCF_distance in pCF_distances:
#         r0=np.array([15,15])
#         x1,y1=np.array(puntos_correlacion(pCF_distance))
#         Matriz=FCS.read_B64(Archivo,Size=[8192*32,32,32])
#         Frames=len(Matriz)
#         Size=len(Matriz[0])
#         Tiempo_pixel=1/10000000
        
#         spri=spriteseparada(Matriz=Matriz,R0=r0,R1=np.array([r0[0]+x1,r0[1]+y1]))
#         taus=tau(R1=[x1,y1],Frames=len(spri[0]),Size=Size,Tiempo_pixel=Tiempo_pixel)
        
#         # ah=spri[0][:100]
#         # fig = plt.figure()
#         # ax = Axes3D(fig)
#         # X = np.array([np.linspace(0, 40, len(ah))])
#         # Y = np.array([np.linspace(0, 0, len(ah))])
#         # X, Y = np.meshgrid(X, Y)
#         # Z = np.array([ah])
#         # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot')
#         # plt.show()
        
#         movil=5
#         i=-1
#         # fig = plt.figure('sprite')
#         # ax = Axes3D(fig)
#         # plt.ion()
#         # for i in range(len(spri)):
#         #     if movil ==0:
#         #         X =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[i]))*x1[i]
#         #         Y =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[i]))*y1[i]
#         #         Z = np.array(spri[i])
#         #     else:
#         #         X =(-np.log10(Tiempo_pixel*pCF_distance) +np.log10(moving_average(taus[i], n=movil)))*x1[i]
#         #         Y =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(moving_average(taus[i], n=movil)))*y1[i]
#         #         Z = np.array(moving_average(spri[i], n=movil))
#         #     ax.plot(X, Y, Z)
#         #     ax.set_xlabel('Dirección')
#         #     ax.set_ylabel('Dirección')
#         #     ax.set_zlabel('PCF')
#         #     ax.set_title('PCF distance=%s, R0=(%s,%s)' %(pCF_distance,r0[0],r0[1]),loc='right')
#         # plt.savefig(Archivo +' pcf %s sprite movil=%s.jpg' %(pCF_distance,movil), dpi=150)
#         # plt.show()
#         # plt.close()
        
        
#         # from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
        
#         plt.figure('PSF individual')
#         if movil ==0:
#             plt.plot(taus[i],spri[i],'.r',label='PCF=%s' %(pCF_distance))
#         else:
#             plt.plot(moving_average(taus[i],n=movil),moving_average(spri[i], n=movil),'.r',label='PCF=%s, movil=%s' %(pCF_distance,movil))
#         plt.xscale('log')
#         plt.ylim([-0.05,0.23])
#         plt.xlim([10**(-4),20])
#         plt.grid()
#         plt.ylabel('PCF')
#         plt.xlabel('tau (s)')
#         plt.legend()
#         plt.savefig(Archivo +' pcf %s individual movil=%s.jpg' %(pCF_distance,movil), dpi=150)
#         plt.show()
#         plt.close()