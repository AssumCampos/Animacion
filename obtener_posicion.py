# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:57:02 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""
#Importamos las bibliotecas necesarias y utilizamos
#la funcion reload para poder añadir las tareas correspondientes

from importlib import reload
from mathutils import Vector

import interpolaciones as inter
reload(inter) 

import generar_aleatorio as genera_alea
reload(genera_alea)

#---------------------------------------------------------
#Funcion de la cual obtenemos la posicion interpolada
def get_pos (accion, fotograma, oscilacion_aleatoria, amplitud, metodo):
    """
    Funcion que nos devuelve un vector con las coordenadas interpoladas segun el frame en el cual se encuentre el objeto

    Parameters
    ----------
    accion : objeto.animation_data.action
        Accion descrita por el objeto
    fotograma : frame
        Frame en el cual se encuentra el objeto
    oscilacion_aleatoria : bpy.context.object.AnimSettings.my_bool
        Si es true se utiliza la frecuencia introducida por el usuario y se le suma un vector aleatorio a la posicion interpolada del objeto
    amplitud : bpy.context.object.AnimSettings.my_amplitud
        Amplitud que introduce el usuario y que se utilizara para el calculo del vector aleatorio
    metodo : bpy.context.object.AnimSettings.my_enum
        Metodo elegido por el usuario, las opciones son Interpolacion_Lineal, Hermite y Catmullrom

    Returns
    -------
    posicion : Vector
        Vector que contiene la posicion interpolada segun los parametros introducidos

    """
    
    #Cogemos la accion del objeto en cada una de sus coordenadas
    accion_X = accion.find('location', index=0)
    accion_Y = accion.find('location', index=1)
    accion_Z = accion.find('location', index=2)
    
    #Calculamos la posicion en la cual deben estar cada una de esas coordenadas del objeto
    posicion1 = inter.interpola_valores(accion_X, metodo, fotograma)
    posicion2 = inter.interpola_valores(accion_Y, metodo, fotograma)
    posicion3 = inter.interpola_valores(accion_Z, metodo, fotograma)
    
    #Creamos el vector posicion en el cual guardaremos la posicion interpolada
    posicion = Vector((posicion1, posicion2, posicion3))
    
    #Si oscilacion_aleatoria == true, entonces calcularemos un vector aleatorio que creara unos movimientos aleatorios que seran realizados durante la trayectoria
    if oscilacion_aleatoria:
        
        #Creamos un vector aleatorio en funcion de la amplitud y la frecuencia
        vector_a = genera_alea.vector_aleatorio(amplitud)
        
        #Le sumamos a cada una de las coordenadas del vector posicion la aleatoriedad calculada en cada una de las coordenadas del vector aleatorio
        posicion[0] = posicion[0] + vector_a[0]
        posicion[1] = posicion[1] + vector_a[1]
        posicion[2] = posicion[2] + vector_a[2]
        
    return posicion
#end get_pos






