# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:32:27 2020

@author: admin
"""
import FCS
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import sprite


#==============================================================================
# Archivos
#==============================================================================
Archivo0=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 11.b64'
Archivo1=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 21.b64'
Archivo2=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 31.b64'
Archivo3=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 1.b64'
Archivo4=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 2.b64'
Archivo5=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 3.b64'
Archivo6=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 4.b64'


#==============================================================================
# Defino variables
#==============================================================================
Archivo=Archivo4
pCF_distance=8
r0=np.array([15,15])
x1,y1=np.array(sprite.puntos_correlacion(pCF_distance))
Matriz=FCS.read_B64(Archivo,Size=[8192*32,32,32])
Frames=len(Matriz)
Size=len(Matriz[0])
Tiempo_pixel=1/10000000


#==============================================================================
# Calculo la sprite a la antigua. No se si funciona, creo que cambie el codigo.
#==============================================================================
spri=sprite.spriteseparada(Matriz=Matriz,R0=r0,R1=np.array([r0[0]+x1,r0[1]+y1]))
taus=sprite.tau(R1=[x1,y1],Frames=len(spri[0]),Size=Size,Tiempo_pixel=Tiempo_pixel)


#==============================================================================
# Grafico con un promedio movil de tanto, recomiendo usar el promedio movil 
# especial. Con i controlo la esprite individual que grafico.
#==============================================================================
movil=5
i=-1
fig = plt.figure('sprite')
ax = Axes3D(fig)
plt.ion()
for i in range(len(spri)):
    if movil ==0:
        X =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[i]))*x1[i]
        Y =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(taus[i]))*y1[i]
        Z = np.array(spri[i])
    else:
        X =(-np.log10(Tiempo_pixel*pCF_distance) +np.log10(moving_average(taus[i], n=movil)))*x1[i]
        Y =(-np.log10(Tiempo_pixel*pCF_distance) + np.log10(moving_average(taus[i], n=movil)))*y1[i]
        Z = np.array(moving_average(spri[i], n=movil))
    ax.plot(X, Y, Z)
    ax.set_xlabel('Dirección')
    ax.set_ylabel('Dirección')
    ax.set_zlabel('PCF')
    ax.set_title('PCF distance=%s, R0=(%s,%s)' %(pCF_distance,r0[0],r0[1]),loc='right')
plt.savefig(Archivo +' pcf %s sprite movil=%s.jpg' %(pCF_distance,movil), dpi=150)
plt.show()
plt.close()

plt.figure('PSF individual')
if movil ==0:
    plt.plot(taus[i],spri[i],'.r',label='PCF=%s' %(pCF_distance))
else:
    plt.plot(sprite.moving_average(taus[i],n=movil),sprite.moving_average(spri[i], n=movil),'.r',label='PCF=%s, movil=%s' %(pCF_distance,movil))
plt.xscale('log')
plt.ylim([-0.05,0.23])
plt.xlim([10**(-4),20])
plt.grid()
plt.ylabel('PCF')
plt.xlabel('tau (s)')
plt.legend()
plt.savefig(Archivo +' pcf %s individual movil=%s.jpg' %(pCF_distance,movil), dpi=150)
plt.show()
plt.close()