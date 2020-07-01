# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 02:34:36 2020

@author: admin
"""
import numpy as np
import test_poisson as p

#==============================================================================
# Valores obtenidos de cuentas de oscuridad, diferentes archivos
#==============================================================================
frecuencia_observada=np.array([13041869,64866,443,19,3]) #mejor medicion
#frecuencia_observada=np.array([248280,1706,13,1]) #Ga spot
#frecuencia_observada=np.array([248874,1120,6]) #Ga spot agua
#frecuencia_observada=np.array([249956,42,2]) #Ga spot laseroff
#frecuencia_observada=np.array([12481159,603453,20711,1419,288,99,32,17,10,5,5,2]) #Ga no de oscuridad

#==============================================================================
# Una tira de valores poisonianos
#==============================================================================
#frecuencia_observada=[]
#Numero_maximo=4 #numero maximo de cuentas observadas en un pixel
#for i in range(Numero_maximo+1):
#    frecuencia_observada.append(p.poison(0.1,i))
#frecuencia_observada=np.array(frecuencia_observada)*10000

numero=np.linspace(0,len(frecuencia_observada)-1,len(frecuencia_observada))
discrepancia,grados_libertad=p.test(frecuencia_observada,numero,restriccion=True,probabilidad1=True)
discrepancia_acepto=p.tabla_chi(0.05,grados_libertad)

if discrepancia>discrepancia_acepto:
    print('Con una significancia de 0.05 rechazamos la hipotesis de que es poisoniana')
    print('discrepancia= %s, discrepancia para aceptar= %s' %(np.round(discrepancia,2),np.round(discrepancia_acepto,2)))
else:
    print('Con una significancia de 0.05 aceptamos la hipotesis de que es poisoniana')
    print('discrepancia=%s' %(np.round(discrepancia,2))) 