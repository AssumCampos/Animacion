# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 20:00:32 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""
#Importamos las bibliotecas necesarias y utilizamos
#la funcion reload para poder añadir las tareas correspondientes

from importlib import reload

import obtener_posicion as obt_pos
reload(obt_pos)

import generar_aleatorio as genera_alea
reload(genera_alea)

import interpolaciones as interpolacion
reload(interpolacion)

import bpy
import math
from mathutils import Vector,Quaternion
from math import sin,cos,acos


def cambio_variable(escena, frm, tabla, vel):
    """
    Obtenemos la velocidad y la distancia actual del panel,
    añadido por el usuario
    """
    
    velocidad = bpy.context.object.AnimSettings.my_tipoVelocidad
    dist_act = bpy.context.object.AnimSettings.distancia_actual

    """
    Dependiendo de qué velocidad sea le pasamos a buscar tabla la distancia 
    añadida por el usuario o la calculada por el frame entre 24 por la velocidad.
    """
    if velocidad == "velCON":
        #Controlamos que si el usuario se pasa de rango de distancia máxima de la trayectoria
        if (dist_act > tabla[-1][1]):
            dist_act = tabla[-1][1]
        frm_barra = buscar_tabla(dist_act, tabla)
    elif velocidad == "velCTE":
        frm_barra = buscar_tabla(((frm/24) * vel) , tabla)        
    else:
        frm_barra = frm
        
    return frm_barra

def generar_tabla():
    
    """
    Funcion que genera la tabla
    
    Parameters
    ----------
        accion : objeto.animation_data.action.fcurves
            Trayectoria que realiza el objeto 
        context: bpy.context
            
    Returns
    -------
        tabla con la posicion de cada frame de la escena
    
    """
    accion = bpy.context.object.animation_data.action.fcurves
    osci = bpy.context.object.AnimSettings.my_bool
    ampli = bpy.context.object.AnimSettings.my_amplitud
    metodo = bpy.context.object.AnimSettings.my_enum
    
    #Creamos la variable tabla vacía y le añadimos el primer frame con la distancia 0
    tabla = []
    elemento_tabla = [bpy.context.scene.frame_start, 0] 
    tabla.append(elemento_tabla)
    
    #Ponemos el frame de nuestra escena en el primer keyframe
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    d_modulo = 0
    
    """
    Recorremos todos los keyframes, desde el primero + 1 hasta el último.
    Obtenemos la posición actual y la anterior con el getpos para que nos devuelvan el frame
    ya interpolado según el método de interpolación selecionado en el panel.
    Después sumamos esta posición a todas las anterior y lo añadimos a la tabla con el frame
    específico en la accion original..
    
    """
    for frm in range(bpy.context.scene.frame_start + 1, bpy.context.scene.frame_end): 
        posicion_actual = obt_pos.get_pos(accion, frm, osci, ampli, metodo)  
        
        posicion_anterior = obt_pos.get_pos(accion, frm-1, osci, ampli, metodo)  
            
        posicion = Vector ((posicion_actual - posicion_anterior))

        d_modulo = d_modulo + posicion.magnitude
        
        elemento_tabla = [frm, d_modulo] 
        tabla.append(elemento_tabla)
    #enf_for
    
    return tabla

def buscar_tabla(l, tabla):
    
    """
    Funcion que busca en la tabla la posicion de un frame
    
    Parameters
    ----------
        
        l: posicion del objeto
        
        tabla: tabla con los valores de las posiciones originales de los frames
        
    Returns
    -------
        valor del frame de la posicion l
    
    """
    frm_devolver = -1
    
    """
    Recorremos toda la tabla hasta que encontremos que la distancia que nos llega
    es pequeña que la distancia que tenemos en la tabla
    """    
    i = 0    
    while i < len(tabla) and tabla[i][1] < l:
        i = i + 1
        
    #Interpolamos linealmente para a partir de la distancia, sacar el frame
    m = (l - tabla[i-1][1]) / (tabla[i][1] - tabla[i-1][1])
    n = tabla[i][0] * m + (1 - m) * tabla[i-1][0]
    
    frm_devolver = n
     
    return frm_devolver

def clamp(x, min, max):
    """ 
    Devuelve el valor x recortado al intervalo [min,max]
    Puede simplificarse en una linea como:
    return min(max(x,min),max)
    """
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x
    
def orientacion(escena, objeto):
    """
    Parameters
    ----------
    escena : bpy.scene
        Escena de nuestro entorno.
    objeto : bpy.context.object
        Objeto de nuestra escena.

    Returns
    -------
    q : Quaternion
        Cuaternion de rotación y lateral.

    """    
    e = bpy.context.object.AnimSettings.eje_inclinacion
    e_l = bpy.context.object.AnimSettings.eje_lateral
    
    if e == "ejeX+":
        e = Vector ((1,0,0))
    elif e == "ejeX-":
        e = Vector ((-1,0,0))
    elif e == "ejeY+":
        e = Vector ((0,1,0))
    elif e == "ejeY-":
        e = Vector ((0,-1,0))
    elif e == "ejeZ+":
        e = Vector ((0,0,1))
    elif e == "ejeZ-":
        e = Vector ((0,0,-1))
        
    if e_l == "ejeX+":
        e_l = Vector ((1,0,0))
    elif e_l == "ejeX-":
        e_l = Vector ((-1,0,0))
    elif e_l == "ejeY+":
        e_l = Vector ((0,1,0))
    elif e_l == "ejeY-":
        e_l = Vector ((0,-1,0))
    elif e_l == "ejeZ+":
        e_l = Vector ((0,0,1))
    elif e_l == "ejeZ-":
        e_l = Vector ((0,0,-1))
    
    # Alinear el objeto con la tangente
    f_actual = escena.frame_current 
    f_anterior = f_actual-1
        
    pos_act = Vector(objeto.location)
    
    escena.frame_set(f_anterior)
    pos_ant = Vector(objeto.location)
     
    t = (pos_act - pos_ant).normalized()
    
    vec = Vector.cross(e,t).normalized()
    
    c1 = clamp(e.dot(t), -1, 1)
    
    theta = acos(c1)

    s = cos(theta/2.0)
    w = sin(theta/2.0)*vec
    
    q1 = Quaternion()
    q1.w = s
    q1.x = w[0]
    q1.y = w[1]
    q1.z = w[2]
 
    # Inclinar el coche lateralmente
    e_l_rotate = Vector(e_l)
    e_l_rotate.rotate(q1)
        
    z = Vector((0, 0, 1))
    l = t.cross(z)
    l.normalize()
   
    c2 = clamp(e_l_rotate.dot(l),-1,1)

    theta_l = acos(c2)
    
    if e_l_rotate[2] < 0:
        theta_l = -theta_l
   
    s = cos(theta_l/2.0)
    w = sin(theta_l/2.0)*t
    
    q2 = Quaternion()
    q2.w = s
    q2.x = w[0]
    q2.y = w[1]
    q2.z = w[2]
    
    
    if bpy.context.object.AnimSettings.inclinacion_bool == True:
        inclinacion = bpy.context.object.AnimSettings.inclinacion
        theta_i = math.pi * inclinacion / 180
        s = cos(theta_i/2.0)
        w = sin(theta_i/2.0)*e
    
        q3 = Quaternion()
        q3.w = s
        q3.x = w[0]
        q3.y = w[1]
        q3.z = w[2]
        
        q = q2 @ q1 @ q3
    else:
        q = q2 @ q1
    
    return q

#------------------------------------
#Funcion que inserta keyframes en las coordenadas interpoladas por la funcion get_pos
def insertar_keyframes(escena, accionfcurves, freq, osci, ampli, metodo, objeto, tabla):
    """
    Funcion que inserta keyframes en las coordenadas interpoladas por la funcion get_pos

    Parameters
    ----------
    escena : bpy.context.scene
        Escena sobre la cual vamos a trabajar
    accionfcurves : objeto.animation_data.action.fcurves
        Trayectoria que realiza el objeto
    freq : bpy.context.object.AnimSettings.my_frecuencia
        Numero de frames que tienen que pasar hasta insertar un keyframe
    osci : bpy.context.object.AnimSettings.my_bool
        Opcion que si es true habilita un vector aleatorio que se sumara a la posicion interpolada para conseguir un movimiento aleatorio mientras sigue la trayectoria
    ampli : bpy.context.object.AnimSettings.my_amplitud
        Tamaño de la oscilacion
    metodo : bpy.context.object.AnimSettings.my_enum
        Metodo de interpolacion que queremos usar
    objeto : bpy.context.object
        Utilizaremos un objeto copia para no modificar el objeto original

    Returns
    -------
    None.

    """
    
    #Suponemos que el usuario pondrá los keyframes siempre en los tres ejes
    kfrm_primer_X = accionfcurves.find('location', index=0).keyframe_points[0].co[0]
    
    #Obtenemos del panel qué tipo de velocidad es la selecionada por el usuario
    tipo_vel = bpy.context.object.AnimSettings.my_tipoVelocidad
    
    #Creamos el inicio y el fin de nuestro recorrido
    ini = int(kfrm_primer_X)
    fin = 0
    
    """
    Dependiendo de nuestra velocidad nuestros parámetros serán unos u otros
    """
    if tipo_vel == 'velCTE' or tipo_vel == 'velCON':
        freq = 1
        if tipo_vel == 'velCON':
            vel = 1
            frame_final  = bpy.context.scene.frame_end
        else:
            vel = bpy.context.object.AnimSettings.my_vel
            print(f"velocidad: {vel}")
            frame_final = int(tabla[-1][1]/vel*24)
            
        fin = frame_final
        bpy.context.scene.frame_end = frame_final
        if bpy.context.scene.frame_end < frame_final:
            bpy.context.scene.frame_end = frame_final
    else:
        freq = bpy.context.object.AnimSettings.my_frecuencia
        fin = bpy.context.scene.frame_end
        vel = 1
        
    print(f"fin: {fin}")
    # Aquí añadimos los fotogramas de posición
    for i in range(ini, fin, freq):
        
        escena.frame_set(i)
        
        #Llamamos a cambio de variable para cambiar el frame a insertar
        frm_barra = cambio_variable(escena, i, tabla, vel)
 
        #Calculamos el vector con las posiciones interpoladas
        vector = obt_pos.get_pos(accionfcurves, frm_barra, osci, ampli, metodo)                
        
        #Colocamos el objeto actual en esa posicion
        objeto.location[0] = vector[0] 
        objeto.location[1] = vector[1] 
        objeto.location[2] = vector[2] 
        
        #Insertamos un keyframe en la posicion actual del objeto
        objeto.keyframe_insert('location', frame=i)
        
    #end for 
    
    # Aquí añadimos los fotogramas de cuaternión
    for j in range (ini+1, fin):
        escena.frame_set(j)
        quat = orientacion(escena, objeto)
        
        objeto.rotation_quaternion.w = quat.w
        objeto.rotation_quaternion.x = quat.x
        objeto.rotation_quaternion.y = quat.y
        objeto.rotation_quaternion.z = quat.z
        
        objeto.keyframe_insert('rotation_quaternion', frame = j)
       
   