# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 00:10:33 2020

@author: admin
"""

import sprite
import numpy as np
import FCS
from matplotlib import pyplot as plt

Archivo0=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 11.b64'
Archivo1=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 21.b64'
Archivo2=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200713\20200713 31.b64'
Archivo3=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 1.b64'
Archivo4=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 2.b64'
Archivo5=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 3.b64'
Archivo6=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 4.b64'

def G_PCF(Matriz,R0,R1,tau_max=80):
    G=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[:,0,0])-j):
            num=num+Matriz[i,R0[0],R0[1]]*Matriz[i+j,R1[0],R1[1]]
        denominador=np.mean(Matriz[:(len(Matriz[:,0,0])-j),R0[0],R0[1]])*np.mean(Matriz[:(len(Matriz[:,0,0])-j),R1[0],R1[1]])
        G.append(num/(denominador*(len(Matriz[:,0,0])-j))-1)
    return np.array(G) 

#==============================================================================
# Defino variables
#==============================================================================
Archivo=Archivo4
pCF_distance=4
R0=np.array([14,14])
# x1,y1=np.array(sprite.puntos_correlacion(pCF_distance))
Matriz=FCS.read_B64(Archivo,Size=32)
Frames=len(Matriz)
Size=len(Matriz[0])
Tiempo_pixel=1/10000000
movil=0
Tipo_movil=True



#==============================================================================
# Grafico la pCF
#==============================================================================
Matriz=FCS.read_B64(Archivo,Size=32)
Matriz=Matriz[:50000,:,:]

sprits=[]
R00=[]
i=0
while i<10*32:
    if i%32==0:
        a=0
        b=int(1*i/32)
    R00.append([a,b])
    a=a+1
    i=i+1

maximo=1000
for i in R00:
    sprits.append(FCS.corrlineal_fft(Matriz[:,R0[0],R0[1]],Matriz[:,i[0],i[1]+pCF_distance])[:maximo])
Tiempo_imagen=Tiempo_pixel*Size**2
taus=np.linspace(0,Frames-1,Frames)*Tiempo_imagen

sprits=np.array(sprits)
spri=[]
sprid=[]
for i in range(len(sprits[0,:])):
    spri.append(np.mean(sprits[:,i]))
    sprid.append(np.std(sprits[:,i]))


# spri,taus=sprite.PCF(Matriz=Matriz,R0=R0,R1=np.array([R0[0],R0[1]+pCF_distance]),Tiempo_pixel=Tiempo_pixel)
# spri=spri[:5000]
# taus=taus[:5000]
# sprim=G_PCF(Matriz,R0,R1=np.array([R0[0],R0[1]+pCF_distance]),tau_max=5000)

plt.figure('PSF individual')
# if movil ==0:
#     plt.plot(taus,spri,'.r',label='PCF=%s' %(pCF_distance))
#     plt.plot(np.array(taus),np.array(sprim),'.b',label='PCFm=%s' %(pCF_distance))
# else:
#     plt.plot(sprite.moving_average(taus,n=movil,Especial=Tipo_movil),sprite.moving_average(spri, n=movil,Especial=Tipo_movil),'-',label='PCF=%s' %(pCF_distance))

plt.plot(taus[:maximo],spri,label='PCF=%s' %(pCF_distance))
plt.errorbar(taus[:maximo],spri,sprid,label='PCF=%s' %(pCF_distance))
plt.plot(taus[:maximo],sprits[0],'.r',label='PCF=%s' %(pCF_distance))

plt.xscale('log')
plt.grid()
plt.ylabel('Correlación')
plt.xlabel('Tiempo de Correlación (s)')
# plt.ylim([0,0.22])
# plt.xlim([10**(-4),0.1])
plt.legend()
# plt.savefig(Archivo +' D=%s pcf individual movil=%s  especial=%s,5.jpg' %(D,movil,Tipo_movil), dpi=250)
plt.show()
# plt.close()