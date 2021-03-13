# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 17:38:25 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""
#Importamos las bibliotecas necesarias y utilizamos

from mathutils import Vector
from numpy.random import random
from random import uniform

#------------------------------------------------------------
#Funcion que calcula un vector aleatorio

def vector_aleatorio (ampli_max):
    """
    Funcion que calcula un vector aleatorio

    Parameters
    ----------
    ampli_max : bpy.context.object.AnimSettings.my_amplitud
        Tamaño de la oscilacion

    Returns
    -------
    vector_aleatorio : Vector
        Vector de tres elementos con valores aleatorio entre 0 y 1

    """

    #Creamos tres valores aleatorios en el intervalo [0,1]
    vector_al1 = random()
    vector_al2 = random()
    vector_al3 = random()
    
    #Creamos un vector de 3 elementos y le asignamos los valores creados
    vector_al = Vector((vector_al1, vector_al2, vector_al3))
    
    
    #Normalizamos el vector aleatorio generado
    Vector.normalize(vector_al)
    
    #Creamos un modulo aleatorio
    modulo_al = uniform(-ampli_max, ampli_max)
    
    #Generamos el nuevo vector aleatorio entre 0 y el modulo aleatorio    
    vector_aleatorio = Vector(( vector_al[0] * modulo_al, vector_al[1] * modulo_al, vector_al[2] * modulo_al))
    
    return vector_aleatorio

    