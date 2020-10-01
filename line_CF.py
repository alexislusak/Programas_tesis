# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:45:58 2020

@author: admin
"""
import FCS
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as col
from mpl_toolkits.mplot3d import Axes3D

def pCF_linea(Matriz,R0,R1,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0,logtime=False,Movil_log=0,Quitar0=True):
    Frames=len(Matriz[:,0,0])
    # Size=len(Matriz[0,:,0])       
    # P0=Matriz[:,R0,0]
    # P1=Matriz[:,R1,0]
    Size=len(Matriz[0,0,:])
    P0=Matriz[:,0,R0]
    P1=Matriz[:,0,R1]
    if Tiempo_imagen==0:
        Tiempo_imagen=Tiempo_pixel*Size+Tiempo_retorno_linea
    if Quitar0==True:
        G=FCS.corrlineal_fft(P0,P1)[1:]
    else:
        G=FCS.corrlineal_fft(P0,P1)
    if max(G)>100:
        G=G*0
    Tiempo_retrazo=(R1-R0)*Tiempo_pixel
    if Quitar0==True:
        Tau=np.linspace(1,int(Frames/2),int(Frames/2)-1)*Tiempo_imagen+Tiempo_retrazo
    else:
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
    # Size=len(Matriz[0,:,0])
    Size=len(Matriz[0,0,:])
    Lineas=[]
    for i in range(Size):
        Lineas.append(pCF_linea(Matriz=Matriz,R0=i,R1=i+PCF,Tiempo_pixel=Tiempo_pixel,Tiempo_retorno_linea=Tiempo_retorno_linea,Tiempo_imagen=Tiempo_imagen))
    return np.array(Lineas)

def pCF_lineasgrid(Matriz,PCF,Tiempo_pixel,Tiempo_retorno_linea=0,Tiempo_imagen=0,logtime=False,Movil_log=0):
    # Size=len(Matriz[0,:,0])
    Size=len(Matriz[0,0,:])
    G=[]
    T=[]
    for i in range(Size-PCF):
        Lineas=pCF_linea(Matriz=Matriz,R0=i,R1=i+PCF,Tiempo_pixel=Tiempo_pixel,Tiempo_retorno_linea=Tiempo_retorno_linea,Tiempo_imagen=Tiempo_imagen,logtime=logtime,Movil_log=Movil_log)
        G.append(Lineas[0])
        T.append(Lineas[1])
    return np.array(G),np.array(T)  

def smoot_horizontal(Matriz,Movil):
    if Movil!=0:
        N_Matriz=[]
        for i in range(len(Matriz[0,:])):
            N_Matriz.append(FCS.moving_average(Matriz[:,i],Movil))
        return np.transpose(np.array(N_Matriz))
    else:
        return Matriz
            


# Archivo=r'C:\Users\admin\Desktop\imagenes\inicio lineas\Line Scan difusion isotropica 2D sin barreras tp_1us - 100 ciclos1.b64'
# Archivo=r'C:\Users\admin\Desktop\imagenes\inicio lineas\line scan usando mascara1.b64' #256
# Archivo=r'C:\Users\admin\Desktop\Line Scan41.b64' #64
Archivo=r'C:\Users\admin\Desktop\tesis de licenciatura\back up manu\2018-11-27\mcherry_6hs_cell2_line_2cells.lsm' #64


Tipo_archivo='lsm' #lsm o b64
Cantidad_lineas=60000
if Tipo_archivo=='lsm':
    Matriz=FCS.read_LSM(Archivo)[:Cantidad_lineas]
else:
    Matriz=FCS.read_B64(Archivo,Size=64,Voltear=False,Line=True)


Tiempo_pixel=3.07*10**(-6) 
PCF=8 #distancia de la PCF
movil=3 #cuanto promediamos al comienzo, tratar de no usar
especial=True #para aplicar el promedio logaritmico
horizontal_movil=3  #usar numeros impares, es el smoot horizontal
 
G,T=pCF_lineasgrid(Matriz=Matriz,PCF=PCF,Tiempo_pixel=Tiempo_pixel,logtime=especial,Movil_log=movil)       
G=smoot_horizontal(G, horizontal_movil)
n=int(np.floor(horizontal_movil/2))
T=T[n:len(T[:,0])-n,:]
Y=[]
if Tipo_archivo=='lsm':
    for i in range(len(G)):
        Y.append(np.ones(len(G[0]))*i)
else:
    for i in range(len(G)):
        Y.append(np.ones(len(G[0]))*(len(G)-i))
X=np.array(T)
Y=np.array(Y)
Z=np.array(G)

mmax=5000 #numero maximo de puntos de tiempo en el plot

#%%       
#==============================================================================
# Grafico de otra manera, es caca
#==============================================================================
# lineas=pCF_lineas(Matriz=Matriz,PCF=PCF,Tiempo_pixel=Tiempo_pixel)
# fig = plt.figure('Alfombra')
# ax = Axes3D(fig)
# plt.ion()
# for i in range(len(lineas[:,0,0])):
#     if movil ==0:
#         X =np.ones(len(lineas[i,1,:]))*i
#         if PCF==0:
#             Y =np.log10(lineas[i,1,:])
#         else:
#             Y =-np.log10(Tiempo_pixel*PCF) + np.log10(lineas[i,1,:])
#         Z = np.array(lineas[i,0,:])
#     else:
#         if PCF==0:
#             Y =np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
#         else:
#             Y =-np.log10(Tiempo_pixel*PCF) + np.log10(FCS.moving_average(lineas[i,1,:], n=movil,Especial=especial))
#         Z = np.array(FCS.moving_average(lineas[i,0,:], n=movil,Especial=especial))
#         X =np.ones(len(Z))*i
#     ax.plot(X, Y, Z)
#     ax.set_xlabel('Posición')
#     ax.set_ylabel('Tiempo de correlación (s)')
#     ax.set_zlabel('Correlación')
#     ax.set_title('PCF distance=%s' %(PCF),loc='right')
#     ax.set_zlim(-0.2,4)
# plt.savefig(Archivo +' pcf %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
# plt.show()
# plt.close()      

#%%
#==============================================================================
# Grafico en 3D funciona, ploteando surface
#==============================================================================
fig = plt.figure('Alfombra2')
ax = Axes3D(fig)
Vmin=0
if min(Z[:,1])>0:
    Vmin=min(Z[:,1])   
a=ax.plot_surface(X=X[:,:mmax], Y=Y[:,:mmax], Z=Z[:,:mmax], cmap=plt.cm.jet, rstride=1, cstride=1,vmin=Vmin,vmax=max(Z[:,1]), linewidth=0, antialiased=False)
fig.colorbar( a, shrink=0.5, anchor=(0.0, 0.5))
ax.set_ylabel('Posición')
ax.set_xlabel('Tiempo de correlación (log10(s))')
ax.set_zlabel('Correlación')
ax.set_title('PCF distance=%s' %(PCF),loc='right')
# ax.set_zlim(-0.05,max(Z[:,1])*1.1)
# plt.savefig(Archivo +' pcf %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
plt.show()
  
#%%
#==============================================================================
# Grafico en 3D funciona, ploteando lineas individuales
#==============================================================================
fig = plt.figure('Alfombra3')
ax = Axes3D(fig)
plt.ion()
mz=max(Z[:,1])
for i in range(len(Z[:,0])):
    for f in range(mmax):
        ax.plot(X[i,f+1:f+1+2],Y[i,f+1:f+1+2], Z[i,f+1:f+1+2], color = plt.cm.jet(Z[i,f+1]/mz))
ax.set_ylabel('Posición')
ax.set_xlabel('Tiempo de correlación (log10(s))')
ax.set_zlabel('Correlación')
ax.set_title('PCF distance=%s' %(PCF),loc='right')
ax.set_zlim(-0.05,max(Z[:,1])*1.1)
# plt.savefig(Archivo +' pcf %s line movil=%s especial=%s.jpg' %(PCF,movil,especial), dpi=150)
plt.show()


#%%       
#==============================================================================
# Grafico una sola linea
#==============================================================================
fig = plt.figure('Alfombra')
ax = Axes3D(fig)
for i in range(10):
    linea=i
    ax.plot(X[linea], Y[linea], Z[linea],'.')
    ax.set_ylabel('Posición')
    ax.set_xlabel('Tiempo de correlación (log10(s))')
    ax.set_zlabel('Correlación')
    ax.set_title('PCF distance=%s' %(PCF),loc='right')
ax.set_zlim(-0.004,0.013)
plt.show()

promedio=1000
matriz_intensidad=[]
for i in range(50000):
    matriz_intensidad.append(sum(Matriz[i:promedio+i,0,:]))
plt.figure('intensidad')
plt.pcolor(matriz_intensidad)