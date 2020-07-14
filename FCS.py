# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 01:51:20 2020

@author: admin
"""
import numpy as np
import numpy.fft
from lfdfiles import SimfcsB64 as lfd

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

#==============================================================================
# Defino la funcion teorica de autocorrelacion
#==============================================================================
def G_teorica3D(N,alpha,D,w0,wz,t):
    G=(alpha/N)*(1+4*D*t/w0**2)**(-1)*(1+(w0/wz)**2*t*4*D/w0**2)**(-0.5)
    return G
def G_teorica2D(N,alpha,D,w0,t):
    G=(alpha/N)*(1+4*D*t/w0**2)**(-1)
    return G

#==============================================================================
# Correlacion de pares usando FFT de forma circular
#==============================================================================
def corrcircular_fft(a, b):
    """Return circular correlation of two arrays using DFT."""
    size = a.size
    # forward DFT
    a = numpy.fft.rfft(a)
    b = numpy.fft.rfft(b)
    # multiply by complex conjugate
    c = a.conj() * b
    # reverse DFT
    c = numpy.fft.irfft(c)    
    # positive delays only
    c = c[:size // 2]   
    # normalize with the averages of a and b
    #   c is already normalized by size
    #   the 0th value of the DFT contains the sum of the signal
    c /= a[0].real * b[0].real / size
    c -= 1.0
    return c

#==============================================================================
# Correlacion de pares usando FFT de forma lineal
#==============================================================================
def corrlineal_fft(a, b):
    """Return linear correlation of two arrays using DFT."""
    size = a.size    
    # subtract mean and pad with zeros to twice the size
    a_mean = a.mean()
    b_mean = b.mean()
    a = numpy.pad(a-a_mean, a.size//2, mode='constant')
    b = numpy.pad(b-b_mean, b.size//2, mode='constant')
    # forward DFT
    a = numpy.fft.rfft(a)
    b = numpy.fft.rfft(b)
    # multiply by complex conjugate
    c = a.conj() * b
    # reverse DFT
    c = numpy.fft.irfft(c)
    # positive delays only
    c = c[:size // 2]        
    # normalize with the averages of a and b
    c /= size * a_mean * b_mean
    return c

#==============================================================================
# Lee un B64 y lo convierte en matriz. Voltear es para que se gire la matriz 
# adecuadamente de los archivos simulador. Se necesita el paquete lfdfiles, se
# instala mediante la promp de anaconda corriendo: pip install lfdfiles --user
#==============================================================================
def read_B64(Archivo,Voltear=True):
    Read=lfd(Archivo)
    Matriz=Read.asarray()
    if Voltear==False:
        return Matriz
    if Voltear==True:
        for i in range(len(Matriz)):
            Matriz[i]=np.transpose(np.rot90(Matriz[i].copy(),-1))
        return Matriz
    else:
        return print('Defina Voltear correctamente, usar True para archivos de simulacion')
        