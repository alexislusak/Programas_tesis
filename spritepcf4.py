# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:40:53 2020

@author: admin
"""

import numpy as np
from matplotlib import pyplot as plt

archivo='3.5hs_pcor_celulas6 hugevector'
hugevector= open(archivo)

def sprite4(Vector,Size,Frames,PosicionX,PosicionY):
    if PosicionX<4 or PosicionX>Size-4 or PosicionY<4 or PosicionY>Size-4:
        return print('La distancia del sprite al borde debe ser mayor a 4 pixels')
    
    Posiciones=[-4*Size-1,-4*Size,-4*Size+1,-3*Size-2,-3*Size+2,-2*Size-3,-2*Size+3,-Size-4,-Size+4,-4,0,+4,Size-4,Size+4,2*Size-3,2*Size+3,3*Size-2,3*Size+2,4*Size-1,4*Size,4*Size+1]
    Posicion_inicial= Size*PosicionX+PosicionY
    
    Linea=Vector.readline()
    Frame_posicion_inicial=int(int(Linea[0:9])%Size**2)
    Frame_numero_inicial=int(np.floor(int(Linea[0:9])/Size**2))
    
    if Frame_posicion_inicial!=0: #esto es un control para que siempre inicie en la posicion 0
        j=0
        while j<Size**2-Frame_posicion_inicial:
            Linea=Vector.readline()
            j=j+1
        Frame_posicion_inicial=int(int(Linea[0:9])%Size**2)
        Frame_numero_inicial=int(np.floor(int(Linea[0:9])/Size**2))
    
    i=0 
    j=0
    k=0
    Intensidad=np.zeros([21,Frames-Frame_numero_inicial])       
    while i < (Frames-Frame_numero_inicial)*Size**2:
        if int(i%Size**2)==Posicion_inicial+Posiciones[j]:
            Intensidad[j][k]=int(Linea[9:17])
            j=j+1
            if j==21:
                j=0
                k=k+1
        Linea=Vector.readline()
        i=i+1
 
    return Intensidad
    
intensidades=sprite4(Vector=hugevector,Size=128,Frames=4000,PosicionX=70,PosicionY=64)

def G_rapida(Matriz,R,tau_max=80):
    numerador=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-j):
            num=num+Matriz[10][i]*Matriz[R][i+j]
        numerador.append(num/(len(Matriz[0])-j))
    denominador=np.mean(Matriz[10])*np.mean(Matriz[R])
    G=numerador/denominador-1
    return G #el posta debe ser dividido por el tiempo entre pixel

G=G_rapida(intensidades,11)   
plt.plot(np.linspace(0,len(G)-1,len(G))*(128**2*10**(-6)),G/(128**2*10**(-6)),'.')   
    
    
#nota: los puntos que fueron adquiridos antes que el punto centro vamos a quitarlo, ya que seria una correlacion a tiempo negativo.
def G(intensidades,Size,Tiempo_pixel,Tiempo_regreso_linea=0,Tiempo_regreso_frame=0):
    Tiempo_entre_pixel=Tiempo_pixel*Size**2+Tiempo_regreso_linea*Size+Tiempo_regreso_frame
##    Tau_inicial=[(-4*Size-1+Size**2)*Tiempo_pixel+(Size-4)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-4*Size+Size**2)*Tiempo_pixel+(Size-4)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-4*Size+1+Size**2)*Tiempo_pixel+(Size-4)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-3*Size-2+Size**2)*Tiempo_pixel+(Size-3)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-3*Size+2+Size**2)*Tiempo_pixel+(Size-3)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-2*Size-3+Size**2)*Tiempo_pixel+(Size-2)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-2*Size+3+Size**2)*Tiempo_pixel+(Size-2)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-Size-4+Size**2)*Tiempo_pixel+(Size-1)*Tiempo_regreso_linea+Tiempo_regreso_imagen,(-Size+4+Size**2)*Tiempo_pixel+(Size-1)*Tiempo_regreso_linea+Tiempo_regreso_imagen,-4,0,4*Tiempo_pixel,(Size-4)*Tiempo_pixel+Tiempo_regreso_linea,(Size+4)*Tiempo_pixel+Tiempo_regreso_linea,(2*Size-3)*Tiempo_pixel+2*Tiempo_regreso_linea,(2*Size+3)*Tiempo_pixel+2*Tiempo_regreso_linea,(3*Size-2)*Tiempo_pixel+3*Tiempo_regreso_linea,(3*Size+2)*Tiempo_pixel+3*Tiempo_regreso_linea,(4*Size-1)*Tiempo_pixel+4*Tiempo_regreso_linea,(4*Size)*Tiempo_pixel+4*Tiempo_regreso_linea,(4*Size+1)*Tiempo_pixel+4*Tiempo_regreso_linea]
    Tau_inicial=[(-4*Size-1)*Tiempo_pixel+(-4)*Tiempo_regreso_linea,(-4*Size)*Tiempo_pixel+(-4)*Tiempo_regreso_linea,(-4*Size+1)*Tiempo_pixel+(-4)*Tiempo_regreso_linea,(-3*Size-2)*Tiempo_pixel+(-3)*Tiempo_regreso_linea,(-3*Size+2)*Tiempo_pixel+(-3)*Tiempo_regreso_linea,(-2*Size-3)*Tiempo_pixel+(-2)*Tiempo_regreso_linea,(-2*Size+3)*Tiempo_pixel+(-2)*Tiempo_regreso_linea,(-Size-4)*Tiempo_pixel+(-1)*Tiempo_regreso_linea,(-Size+4)*Tiempo_pixel+(-1)*Tiempo_regreso_linea,-4*Tiempo_pixel,0,4*Tiempo_pixel,(Size-4)*Tiempo_pixel+Tiempo_regreso_linea,(Size+4)*Tiempo_pixel+Tiempo_regreso_linea,(2*Size-3)*Tiempo_pixel+2*Tiempo_regreso_linea,(2*Size+3)*Tiempo_pixel+2*Tiempo_regreso_linea,(3*Size-2)*Tiempo_pixel+3*Tiempo_regreso_linea,(3*Size+2)*Tiempo_pixel+3*Tiempo_regreso_linea,(4*Size-1)*Tiempo_pixel+4*Tiempo_regreso_linea,(4*Size)*Tiempo_pixel+4*Tiempo_regreso_linea,(4*Size+1)*Tiempo_pixel+4*Tiempo_regreso_linea]

        
    
    
    
    
    
    