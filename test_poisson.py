# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:19:55 2020

@author: admin
"""

import numpy as np

#==============================================================================
# Funcion de poisson
#==============================================================================
def poison(lamda,k):
    return (np.exp(-lamda))*(lamda**k)/(np.math.factorial(k))

#==============================================================================
# Test de hipotesis poisson
#==============================================================================
def test(frecuencia_observada,numero,restriccion=False,probabilidad1=False): #la restriccion es para poner un minimo de frecuencia de 5
    valor_medio=sum(frecuencia_observada*numero)/sum(frecuencia_observada)
    probabilidades=np.empty(len(frecuencia_observada))
    for i in range(len(probabilidades)):
        probabilidades[i]=poison(valor_medio,i)
    if probabilidad1==True: #sirve para que la probabilidad de uno, le suma toda la probabilidad que resta al ultimo
        probabilidades[-1]=1-sum(probabilidades[:(len(probabilidades)-1)])
    frecuencia_esperada=sum(frecuencia_observada)*probabilidades
    if restriccion==True:
        while frecuencia_esperada[-1]<5:
            frecuencia_esperada[-2]=frecuencia_esperada[-2]+frecuencia_esperada[-1]
            frecuencia_esperada=np.delete(frecuencia_esperada,-1)
            frecuencia_observada[-2]=frecuencia_observada[-2]+frecuencia_observada[-1]
            frecuencia_observada=np.delete(frecuencia_observada,-1)
    discrepancia=sum((frecuencia_observada-frecuencia_esperada)**2/frecuencia_esperada)
    grados_libertad=len(frecuencia_observada)-2
    return discrepancia, grados_libertad

#==============================================================================
# Tabla con valores de chi cuadrado, hasta ahora solo de 0,5 de significancia
#==============================================================================
def tabla_chi(significancia,grados_libertad):
    if significancia==0.05:
        tabla=[3.8415,5.9915,7.8147,9.4877,11.0705]
        return tabla[grados_libertad-1]
    return print('no esta el valor en la tabla')
   