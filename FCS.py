# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 01:51:20 2020

@author: admin
"""
import numpy as np
#from matplotlib import pyplot as plt
#from statsmodels.tsa.stattools import acf as acf

#==============================================================================
# Con este programa podes extraer un pixel del huge vector. Ademas podes
# extraer con el parametro cantidad, la cantidad de pixeles contiguos que 
# quieras
#==============================================================================
def ACF_hugevector(Archivo,Size,Frames,PosicionX,PosicionY,Cantidad):
    Vector= open(Archivo)
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
    Posiciones=np.linspace(0,Cantidad-1,Cantidad)
    Posicion_inicial= Size*PosicionX+PosicionY
    i=0 
    j=0
    k=0
    Intensidad=np.zeros([Cantidad,Frames-Frame_numero_inicial])       
    while i < (Frames-Frame_numero_inicial)*Size**2:
        if int(i%Size**2)==Posicion_inicial+Posiciones[j]:
            Intensidad[j][k]=int(Linea[9:17])
            j=j+1
            if j==Cantidad:
                j=0
                k=k+1
        Linea=Vector.readline()
        i=i+1
    return Intensidad

#==============================================================================
# Funcion de autocorrelacion. La normalizacion depende de cada punto, el
# denominador se divide por la media hasta la cantidad de tiempos usados en el
# numerador.
#==============================================================================
def G_ACF(Matriz,L,tau_max,Tiempo_imagen):
    G=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-j):
            num=num+Matriz[L][i]*Matriz[L][i+j]
        denominador=np.mean(Matriz[L][:(len(Matriz[0])-j)])**2
        G.append(num/(denominador*(len(Matriz[0])-j))-1)
    return np.array(G) 

#==============================================================================
# Funcion de autocorrelacion. La normalizacion es igual para todos los puntos
#==============================================================================
def G_ACF2(Matriz,L,tau_max,Tiempo_imagen):
    numerador=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-j):
            num=num+Matriz[L][i]*Matriz[L][i+j]
        numerador.append(num/(len(Matriz[0])-j))
    denominador=np.mean(Matriz[L][:(len(Matriz[0])-tau_max)])**2
    numerador=np.array(numerador)
    G=numerador/denominador-1
    return G 

#==============================================================================
# Funcion de autocorrelacion. La normalizacion es igual para todos los puntos
#==============================================================================
def G_ACF3(Matriz,L,tau_max,Tiempo_imagen):
    numerador=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-tau_max):
            num=num+Matriz[L][i]*Matriz[L][i+j]
        numerador.append(num/(len(Matriz[0])-tau_max))
    denominador=np.mean(Matriz[L][:(len(Matriz[0])-tau_max)])**2
    numerador=np.array(numerador)
    G=numerador/denominador-1
    return G 

#==============================================================================
# Funcion de correlacion de pares. La normalizacion depende de cada punto, el
# denominador se divide por la media hasta la cantidad de tiempos usados en el
# numerador.
#==============================================================================
def G_PCF(Matriz,R0,R1,tau_max=80):
    G=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-j):
            num=num+Matriz[R0][i]*Matriz[R1][i+j]
        denominador=np.mean(Matriz[R0][:(len(Matriz[0])-j)])*np.mean(Matriz[R1][:(len(Matriz[0])-j)])
        G.append(num/(denominador*(len(Matriz[0])-j))-1)
    return np.array(G)     

#==============================================================================
# Funcion de correlacion de pares. La normalizacion es igual para todos los 
# puntos
#==============================================================================
def G_PCF2(Matriz,R0,R1,tau_max=80):
    numerador=[]
    for j in range(tau_max):
        num=0
        for i in range(len(Matriz[0])-j):
            num=num+Matriz[R0][i]*Matriz[R1][i+j]
        numerador.append(num/(len(Matriz[0])-j))
    denominador=np.mean(Matriz[R0][:(len(Matriz[0])-tau_max)])*np.mean(Matriz[R1][:(len(Matriz[0])-tau_max)])
    G=numerador/denominador-1
    return G 

#retrazo=1000
#i=1
#intensidad2=np.loadtxt('vector de intensidades 20200626 3.csv',delimiter=',')
#intensidad1=np.loadtxt('vector de intensidades 20200626 3.csv',delimiter=',')
#while i<=retrazo:
#    intensidad1=np.delete(intensidad1,-1)
#    intensidad1=np.append(intensidad2[-i],intensidad1)
#    i=i+1
#
#R0=0
#R1=1
#size=8
#tiempo_pixel=10**(-5)
#tiempo_imagen=size**2*tiempo_pixel
#tau_max=5000
#frames=25000 
#
#G=G_PCF([intensidad2,intensidad1],R0,R1,tau_max=tau_max)
#
#plt.figure('al revez')
#plt.plot(np.linspace(0,len(G)-1,len(G))*tiempo_imagen,G,'.',label='Paircorr')
#r=retrazo*tiempo_imagen
#plt.plot([r,r],[0,max(G)],'g',label='Retrazo= %s s' %(r))
#plt.xscale('log')
#plt.ylabel('PCF')
#plt.xlabel('tiempo (s)')
#plt.grid()
#plt.legend()
