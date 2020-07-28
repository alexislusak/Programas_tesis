# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 20:38:24 2020

@author: admin
"""

def particulasPSF3D(concentracion_molar,volumenPSF=0.18455):
    micro3alitro=1e-15
    numeroavogadro=6.022*10**23
    particulaslitro=concentracion_molar*numeroavogadro
    volumenPSFlitro=volumenPSF*micro3alitro
    return  volumenPSFlitro*particulaslitro

def particulasPSF2D(moleculas_um2,areaPSF=0.0987):
    return  moleculas_um2*areaPSF

def concentracion3D(moleculas_um2,areaPSF=0.0987,volumenPSF=0.18455):
    particulasPSC=moleculas_um2*areaPSF
    micro3alitro=1e-15
    volumenPSFlitro=volumenPSF*micro3alitro   
    numeroavogadro=6.022*10**23
    concentracion_molar= particulasPSC/(volumenPSFlitro*numeroavogadro)
    return concentracion_molar

moleculas_um2=16    
print(particulasPSF2D(moleculas_um2))    
print(concentracion3D(moleculas_um2))
