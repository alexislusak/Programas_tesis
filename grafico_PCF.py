# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:37:04 2020

@author: admin
"""


import sprite
import numpy as np
import FCS
from matplotlib import pyplot as plt

#==============================================================================
# Grafico en funcion de la pCF distance
#==============================================================================
def graficoPCF_distance(Archivo,pCF_distances,R0,Size,Frames,Clock,movil=0,Tipo_movil=False,D=0):
    Tiempo_pixel=1/Clock
    Matriz=FCS.read_B64(Archivo,Size=[Frames,Size,Size])
    spri=[]
    taus=[]
    for i in pCF_distances:
        # if R0[1]+i>Size:
        #     return print('La pCF distance %s es mayor que el Size. Se sugiere cambiar R0' %(i))
        a,b=sprite.PCF(Matriz=Matriz,R0=R0,R1=np.array([R0[0],R0[1]+i]),Tiempo_pixel=Tiempo_pixel)
        spri.append(a)
        taus.append(b)

    plt.figure('PSF individual')
    if movil ==0:
        for i in range(len(pCF_distances)):
            plt.plot(taus[i],spri[i],'-',label='PCF=%s' %(pCF_distances[i]))
    else:
        for i in range(len(pCF_distances)):
            plt.plot(sprite.moving_average(taus[i],n=movil,Especial=Tipo_movil),sprite.moving_average(spri[i], n=movil,Especial=Tipo_movil),'-',label='PCF=%s' %(pCF_distances[i]))
    if D!=0:
        plt.title('D=%s' %(D))
    plt.xscale('log')
    plt.grid()
    plt.ylabel('Correlación')
    plt.xlabel('Tiempo de Correlación (s)')
    # plt.ylim([0,0.22])
    # plt.xlim([10**(-4),0.1])
    plt.legend()
    plt.savefig(Archivo +' D=%s pcf individual movil=%s  especial=%s,5.jpg' %(D,movil,Tipo_movil), dpi=250)
    plt.show()
    plt.close()

#==============================================================================
# Grafico en funcion de la D
#==============================================================================    
def graficoPCF_D(Archivos,pCF_distance,D,R0,Size,Frames,Clock,movil=0,Tipo_movil=False):
    Tiempo_pixel=1/Clock
    spri=[]
    taus=[]
    for i in Archivos:
        Matriz=FCS.read_B64(i,Size=[Frames,Size,Size])
        if R0[1]+pCF_distance>Size:
            return print('La pCF distance %s es mayor que el Size. Se sugiere cambiar R0' %(i))
        a,b=sprite.PCF(Matriz=Matriz,R0=R0,R1=np.array([R0[0]+pCF_distance,R0[1]]),Tiempo_pixel=Tiempo_pixel)
        spri.append(a)
        taus.append(b)

    plt.figure('PSF individual')
    if movil ==0:
        for i in range(len(Archivos)):
            plt.plot(taus[i],spri[i],'-',label='D=%s' %(D[i]))
    else:
        for i in range(len(Archivos)):
            plt.plot(sprite.moving_average(taus[i],n=movil,Especial=Tipo_movil),sprite.moving_average(spri[i], n=movil,Especial=Tipo_movil),'-',label='D=%s' %(D[i]))
    plt.xscale('log')
    plt.grid()
    plt.title('pCF distancia= %s' %(pCF_distance))
    plt.ylabel('Correlación')
    plt.xlabel('Tiempo de Correlación (s)')
    # plt.ylim([0,0.04])
    plt.legend()
    plt.savefig(Archivos[0] +' pcf=%s movil=%s especial=%s.jpg' %(pCF_distance,movil,Tipo_movil), dpi=250)
    plt.show()
    plt.close()


#==============================================================================
# Grafico en funcion de la concentracion
#==============================================================================
def graficoPCF_concentracion(Archivos,pCF_distance,Concentraciones,R0,Size,Frames,Clock,movil=0,Tipo_movil=False):
    Tiempo_pixel=1/Clock
    spri=[]
    taus=[]
    for i in Archivos:
        Matriz=FCS.read_B64(i,Size=[Frames,Size,Size])
        if R0[1]+pCF_distance>Size:
            return print('La pCF distance %s es mayor que el Size. Se sugiere cambiar R0' %(i))
        a,b=sprite.PCF(Matriz=Matriz,R0=R0,R1=np.array([R0[0]+pCF_distance,R0[1]]),Tiempo_pixel=Tiempo_pixel)
        spri.append(a)
        taus.append(b)

    plt.figure('PSF individual')
    if movil ==0:
        for i in range(len(Archivos)):
            plt.plot(taus[i],spri[i],'-',label='Conc.=%s nM' %(Concentraciones[i]))
    else:
        for i in range(len(Archivos)):
            plt.plot(sprite.moving_average(taus[i],n=movil,Especial=Tipo_movil),sprite.moving_average(spri[i], n=movil,Especial=Tipo_movil),'-',label='Conc.=%s nM' %(Concentraciones[i]))
    plt.xscale('log')
    plt.grid()
    plt.title('pCF distancia= %s' %(pCF_distance))
    plt.ylabel('Correlación')
    plt.xlabel('Tiempo de Correlación (s)')
    # plt.ylim([0,0.04])
    plt.legend()
    plt.savefig(Archivos[0] +' pcf=%s movil=%s especial=%s.jpg' %(pCF_distance,movil,Tipo_movil), dpi=250)
    plt.show()
    plt.close()

#%%
Archivo4=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 2.b64'
Archivo5=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 3.b64'
Archivo6=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200715\20200715 4.b64'

    
R0=np.array([18,10])
Frames=8192*32
Size=32
Clock=10000000
movil=3
Tipo_movil=True
Archivo=Archivo5
D=10
pCF_distances=[4,6,8,10,12]
graficoPCF_distance(Archivo,pCF_distances,R0,Size,Frames,Clock,movil,Tipo_movil,D)

# Archivos=[Archivo6,Archivo4,Archivo5]
# D=[0.1,1,10]
# pCF_distance=8
# graficoPCF_D(Archivos,pCF_distance,D,R0,Size,Frames,Clock,movil,Tipo_movil)

#%%
Archivo1=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 1.b64'
Archivo2=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 2.b64'
Archivo3=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 3.b64'
Archivo4=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 4.b64'
Archivo5=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 5.b64'
Archivo6=r'C:\Users\admin\Desktop\tesis de licenciatura\simulaciones Sim\simulacion 20200723\20200723 6.b64'

    
R0=np.array([15,15])
Frames=4096*32
Size=32
Clock=7500000
movil=3
Tipo_movil=True
# Archivos=[Archivo1,Archivo2,Archivo3,Archivo4,Archivo5,Archivo6]
# Concentraciones=[3.55,7.10,14.21,21.31,42.63,85.26]
Archivos=[Archivo3,Archivo4,Archivo5,Archivo6]
Concentraciones=[14.21,21.31,42.63,85.26]
pCF_distance=8


graficoPCF_concentracion(Archivos,pCF_distance,Concentraciones,R0,Size,Frames,Clock,movil,Tipo_movil)

# Tiempo_pixel=1/Clock
# dispersion=[]
# G0=[]
# maximocola=[]
# for i in Archivos:
#     Matriz=FCS.read_B64(i,Size=[Frames,Size,Size])
#     if R0[1]+pCF_distance>Size:
#         print('La pCF distance %s es mayor que el Size. Se sugiere cambiar R0' %(i))
#     a,b=sprite.PCF(Matriz=Matriz,R0=R0,R1=np.array([R0[0]+pCF_distance,R0[1]]),Tiempo_pixel=Tiempo_pixel)
#     dispersion.append(np.std(a[int(Clock/2048):]))
#     G0.append(max(a[:int(Clock/10240)]))
#     maximocola.append((max(a[int(Clock/2048):])))
    
    
