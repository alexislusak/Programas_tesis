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

print(particulasPSF3D(concentracion_molar=2.23*10**(-9)))
print(particulasPSF2D(moleculas_um2=19.2))