# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 09:19:51 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""

#Importamos las bibliotecas necesarias y utilizamos
#la funcion reload para poder añadir las tareas correspondientes

import bpy 

from importlib import reload

import insertar_fotogramas as insert_f
reload(insert_f)

import generar_aleatorio as genera_alea
reload(genera_alea)

def limpiar_keyframes(obj):
    
    kfrm_pos_X = obj.animation_data.action.fcurves.find('location', index=0)
    kfrm_pos_Y = obj.animation_data.action.fcurves.find('location', index=1)
    kfrm_pos_Z = obj.animation_data.action.fcurves.find('location', index=2)
    
    obj.animation_data.action.fcurves.remove(kfrm_pos_X)
    obj.animation_data.action.fcurves.remove(kfrm_pos_Y)
    obj.animation_data.action.fcurves.remove(kfrm_pos_Z)
    
    return obj

#end limpiar_keyframes


#---------------------------------------------------------------------------------------------
#Funcion que obtiene todos los valores y comienza con la ejecucion del programa principal

def main(tabla):
    """
    Funcion que obtiene todos los valores y comienza con la ejecucion del programa principal

    Returns
    -------
    None.

    """    
    #Variables que podremos editar desde el panel y que son necesarias para ejecutar el programa
    oscilacion = bpy.context.object.AnimSettings.my_bool
    amplitud = bpy.context.object.AnimSettings.my_amplitud
    frecuencia_n = bpy.context.object.AnimSettings.my_frecuencia
    metodo = bpy.context.object.AnimSettings.my_enum
    copias = bpy.context.object.AnimSettings.copias
    
    objeto = bpy.context.object
    
    escena = bpy.context.scene
    base_collection = escena.collection
    collection_name = "Copias de "+objeto.name
    copies_collection = bpy.data.collections.new(collection_name)
    base_collection.children.link(copies_collection)

    accion = objeto.animation_data.action
    
    bpy.context.scene.frame_end = objeto.animation_data.action.fcurves.find('location', index=0).keyframe_points[-1].co[0]
    
    for i in range(0, copias):
        """
        Bucle for que recorre el contador de las copias, para cada una, 
        copia el objeto y su trayectoria, elimina los keyframes de la
        trayectoria copiada y llama a la funcion insertar_keyframes, 
        que inserta los nuevos keyframes de la trayectoria de la copia
        
        """
        objeto_copia = objeto.copy()
        
        copies_collection.objects.link(objeto_copia)
        
        objeto_copia.animation_data.action = accion.copy()
        
        objeto_copia = limpiar_keyframes(objeto_copia)
        
        insert_f.insertar_keyframes(escena, accion.fcurves, frecuencia_n, oscilacion, amplitud, metodo, objeto_copia, tabla)
        
    #end for
    for j in range(bpy.context.scene.frame_start+1, bpy.context.scene.frame_end):
        
        escena.frame_set(j)
        
        quat = insert_f.orientacion(escena, bpy.context.object)
        
        bpy.context.object.rotation_quaternion.w = quat.w
        bpy.context.object.rotation_quaternion.x = quat.x
        bpy.context.object.rotation_quaternion.y = quat.y
        bpy.context.object.rotation_quaternion.z = quat.z
        
        bpy.context.object.keyframe_insert('rotation_quaternion', frame = j)
#end main







