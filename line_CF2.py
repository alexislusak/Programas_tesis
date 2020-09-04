# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 00:09:20 2020

@author: admin
"""


import FCS
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def pCF_linea(Matriz,R0,R1,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0,logtime=False,Movil_log=0):
    Frames=len(Matriz[:,0,0])
    Size=len(Matriz[0,:,0])   
    # Size=len(Matriz[0,0,:])    
    P0=Matriz[:,R0,0]
    # P0=Matriz[:,0,R0]
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size+Tiempo_retorno_linea
    G=FCS.corrlineal_fft(P0,Matriz[:,R1,0])
    if max(G)>100:
        G=G*0
    # G=FCS.corrlineal_fft(P0,Matriz[:,0,R1])
    Tiempo_retrazo=(R1-R0)*Tiempo_pixel
    Tau=np.linspace(0,int(Frames/2)-1,int(Frames/2))*Tiempo_imagen+Tiempo_retrazo
    if Movil_log==0:
        if logtime==False:
            return np.array(G),np.array(Tau)
        if logtime==True:
            Tau=np.log10(Tau)
            return np.array(G),np.array(Tau)
    else:
        G=FCS.moving_average(G,Movil_log,Especial=True)
        if logtime==False:
            Tau=FCS.moving_average(Tau,Movil_log,Especial=True)
        if logtime==True:
            Tau=np.log10(FCS.moving_average(Tau,Movil_log,Especial=True))
        return np.array(G),np.array(Tau)
    
    
def pCF_lineas(Matriz,PCF,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0):
    Size=len(Matriz[0,:,0])
    Lineas=[]
    for i in range(Size):
        Lineas.append(pCF_linea(Matriz=Matriz,R0=i,R1=i+PCF,Tiempo_pixel=Tiempo_pixel,Tiempo_retorno_linea=Tiempo_retorno_linea,Tiempo_imagen=Tiempo_imagen))
    return np.array(Lineas)

def pCF_lineasgrid(Matriz,PCF,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0,logtime=False,Movil_log=0):
    Size=len(Matriz[0,:,0])
    # Size=len(Matriz[0,0,:])
    G=[]
    T=[]
    for i in range(Size):
        Lineas=pCF_linea(Matriz=Matriz,R0=i,R1=i+PCF,Tiempo_pixel=Tiempo_pixel,Tiempo_retorno_linea=Tiempo_retorno_linea,Tiempo_imagen=Tiempo_imagen,logtime=logtime,Movil_log=Movil_log)
        G.append(Lineas[0])
        T.append(Lineas[1])
    return np.array(G),np.array(T)  

def smoot_horizontal(Matriz,Movil):
    N_Matriz=[]
    for i in range(len(Matriz[0,:])):
        N_Matriz.append(FCS.moving_average(Matriz[:,i],Movil))
    return np.transpose(np.array(N_Matriz))
        


# Archivo=r'C:\Users\admin\Desktop\inicio lineas\Line Scan difusion isotropica 2D sin barreras tp_1us - 100 ciclos1.b64'
Archivo=r'C:\Users\admin\Desktop\inicio lineas\line scan usando mascara1.b64'
Matriz=FCS.read_B64(Archivo,Size=256,Voltear=False,Line=True)
Tiempo_pixel=10**(-6)
PCF=0


lineas=pCF_lineas(Matriz=Matriz,PCF=PCF,Tiempo_pixel=Tiempo_pixel)       

        
movil=3
horizontal_movil=25
especial=True
colores=True #para hacer los colores a mano

fig = plt.figure('Alfombra')
ax = Axes3D(fig)
plt.ion()

mz=2
for i in range(len(lineas[:,0,0])):
    if movil ==0:
        if PCF==0:
            Y =np.log10(lineas[i,1,1:])
            Y=np.append(0,Y)
        else:
            Y =-np.log10(Tiempo_pixel*PCF) + np.log10(lineas[i,1,:])
        Z = np.array(lineas[i,0,:])
    else:
        if PCF==0:
            Y =np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
        else:
            Y =-np.log10(Tiempo_pixel*PCF) + np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
        Z = np.array(FCS.moving_average(lineas[i,0,:], n=movil,Especial=especial))
    if colores==True:
        # a=1
        for f in range(50):
            # if i==1000:
            #     a=50
            # f=int((i-1000)*a+1000)
            ax.plot(Y[f:f+2],[i+int(np.floor(horizontal_movil/2)),i+int(np.floor(horizontal_movil/2))], Z[f:f+2], color = plt.cm.jet(Z[f]/mz))
ax.set_xlabel('Posición')
ax.set_ylabel('Tiempo de correlación (s)')
ax.set_zlabel('Correlación')
ax.set_title('PCF distance=%s' %(PCF),loc='right')
ax.set_zlim(-0.2,2)
# plt.savefig(Archivo +' pcf22 %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
plt.show()
# plt.close()      

# G,T=pCF_lineasgrid(Matriz=Matriz,PCF=PCF,Tiempo_pixel=Tiempo_pixel,logtime=especial,Movil_log=movil)       

# horizontal_movil=25  #usar numeros impares
# G=smoot_horizontal(G, horizontal_movil)
# n=int(np.floor(horizontal_movil/2))
# T=T[n:len(T[:,0])-n,:]

# Y=[]
# for i in range(len(G)):
#     Y.append(np.ones(len(G[0]))*i)
#==============================================================================
# Grafico en 3D funciona
#==============================================================================
# X=np.array(T)
# Y=np.array(Y)
# Z=np.array(G)
# mz=max(Z)
# fig = plt.figure('Alfombra2')
# ax = Axes3D(fig)
# if colores==True:
#     a=1
#     for i in range(2000):
#         if i==1000:
#             a=50
#         f=int((i-1000)*a+1000)
#         ax.plot(X[f:f+2], Y[f:f+2], Z[f:f+2], color = plt.cm.jet(Z[f]/mz))
# else:
#     ax.plot_surface(X=np.array(T), Y=np.array(Y), Z=np.array(G), cmap=plt.cm.jet, linewidth=0, antialiased=False)
# fig.colorbar( a, shrink=0.5, anchor=(0.0, 0.5))
# ax.set_ylabel('Posición')
# ax.set_xlabel('Tiempo de correlación (log10(s))')
# ax.set_zlabel('Correlación')
# ax.set_title('PCF distance=%s' %(PCF),loc='right')
# ax.set_zlim(-0.2,10)
# # ax.set_xscale('log') 
# # plt.savefig(Archivo +' pcf %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
# plt.show()

