"""
Created on Fri Oct 16 17:57:02 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""
import bpy

#------------------------------------------------------------------------
# Distribuye las interpolaciones segun la variable metodo

def interpola_valores (c, metodo, num_fotograma) :
    """   
    Distribuye las interpolaciones segun la variable metodo
    
    Parameters
    ----------
    c : bpy.context.object.animation_data.action.fcurves
        Acción del objeto a interpolar.
    metodo : string
        Tipo de método de interpolación.
    num_fotograma : int
        Distancia que encontramos entre los nuevos keyframes,
        obtenidos mediante la interpolación.

    Returns
    -------
    None.

    """    

    if metodo == "lineal":    
        pos = inter_lineal(c, num_fotograma)
        return pos
    
    elif metodo == "hermite":
        pos = inter_hermite(c, num_fotograma)
        return pos
        
    elif metodo == "catmullrom":
        pos = inter_catmullrom(c, num_fotograma)
        return pos
    
#end interpola_valores

#------------------------------------------------------------------------
# Interpola linealmente el objeto que recibe

def inter_lineal (c, num_fotograma):
    """
    Interpola de forma lineal el objeto que recibe

    Parameters
    ----------
    c : bpy.context.object.animation_data.action.fcurves
        Acción del objeto a interpolar.
    num_fotograma : int
        Fotograma a interpolar.

    Returns
    -------
    pos : float
        Nueva posición del objeto interpolado.

    """
    pos = 0
    # Recorremos el vector de keyframes de la acción
    for i in range(0, len(c.keyframe_points)) :
        keyf = c.keyframe_points[i].co[0]
        # Comprobamos que el fotograma que vamos a estudiar tiene un keyframe antes
        if (keyf > num_fotograma):
            # Guardamos las variables del keyframe anterior y posterior
            kfrm_posterior = c.keyframe_points[i]
            kfrm_anterior = c.keyframe_points[i-1]
            
            # Calculamos la pendiente 
            m = (kfrm_posterior.co[1] - kfrm_anterior.co[1])/ (kfrm_posterior.co[0] - kfrm_anterior.co[0]) 
            n = kfrm_anterior.co[1] - m * kfrm_anterior.co[0]
            
            pos = m*num_fotograma+n
            break
        
    return pos
    
#end 


def inter_hermite(c, num_fotograma):
    """
    Interpola con la interpolación Hermite el objeto que recibe    

    Parameters
    ----------
    c : bpy.context.object.animation_data.action.fcurves
        Acción del objeto a interpolar.
    num_fotograma : int
        Fotograma a interpolar.

    Returns
    -------
    pos : float
        Nueva posición del objeto interpolado.

    """
    # Obtenemos la velocidad 
    veloc = c.keyframe_points
    t = num_fotograma/24
    pos = 0
    # Recorremos el vector de keyframes de la acción
    for i in range(0, len(c.keyframe_points)) :
        keyf = c.keyframe_points[i].co[0]
        # Comprobamos que el fotograma que vamos a estudiar tiene un keyframe antes
        if (keyf > num_fotograma):
            # Calculamos los kfrm anteriores, su tiempo
            kfrm_anterior = c.keyframe_points[i-1]
            t_anterior = kfrm_anterior.co[0] / 24.0
            
            # La velocidad la sacamos con los handle
            veloc_ant = veloc[i-1].handle_right[0] / 24.0
          
            # Calculamos los kfrm posterior, su tiempo
            kfrm_posterior = c.keyframe_points[i]
            t_posterior = kfrm_posterior.co[0] / 24.0
            
            # La velocidad la sacamos con los handle
            veloc_post = veloc[i].handle_right[0] / 24.0

            # Sacamos la u 
            u = (t - t_anterior )/(t_posterior - t_anterior)
            # Calculamos la posición
            pos = (1 - 3*u*u + 2*u*u*u)* kfrm_anterior.co[1] + u*u*(3 - 2*u)*kfrm_posterior.co[1] + u*(u - 1)*(u - 1)* veloc_ant + u*u*(u - 1)*veloc_post  
          
            break
       
    return pos
#end

def inter_catmullrom(c, num_fotograma):
    """
    Interpola con la interpolación de Catmull-Rom el objeto que recibe

    Parameters
    ----------
   c : bpy.context.object.animation_data.action.fcurves
        Acción del objeto a interpolar.
    num_fotograma : int
        Fotograma a interpolar.

    Returns
    -------
    pos : float
        Nueva posición del objeto interpolado.

    """
    # Sacamos tau con opción del panel
    tau = bpy.context.object.AnimSettings.my_tau 
    t = num_fotograma/ 24
    pos = 0
    
    # Recorremos el vector de keyframes de la acción
    for i in range(0, len(c.keyframe_points)) :
         keyf = c.keyframe_points[i].co[0]
         
         # Comprobamos que el fotograma que vamos a estudiar tiene un keyframe antes
         if (keyf > num_fotograma):  
             # Comprobamos si está en el primer intervalo
             if c.keyframe_points[i-1].co[0] == c.keyframe_points[0].co[0]:
                 # Cambiamos los valores para que interpolen con el primero y no con el anterior
                 kfrm_anterior2 = c.keyframe_points[i-1] 
                 kfrm_posterior2 = c.keyframe_points[i+1] 
             # Comprobamos si está en el último intervalo    
             elif c.keyframe_points[i].co[0] == c.keyframe_points[len(c.keyframe_points)-1].co[0]:
                 # Cambiamos los valores para que interpolen con el último y no con el posterior
                 kfrm_posterior2 = c.keyframe_points[i]
                 kfrm_anterior2 = c.keyframe_points[i-2] 
                 
             # Sino mantenemos las variables como serían    
             else:
                 
                 kfrm_anterior2 = c.keyframe_points[i-2] 
                 kfrm_posterior2 = c.keyframe_points[i+1] 
                    
             kfrm_anterior = c.keyframe_points[i-1] 
             kfrm_posterior = c.keyframe_points[i] 
             
             # Las cambiamos a tiempo
             t_anterior = kfrm_anterior.co[0] / 24
             t_posterior = kfrm_posterior.co[0] / 24
             
             # Creamos la u
             u = (t - t_anterior )/(t_posterior - t_anterior)
             
             # Hacemos la matriz de Catmull-Rom
             pos1 = kfrm_anterior2.co[1] * (-tau * u + 2 * tau * u * u - tau * u * u *u) 
             pos2 = kfrm_anterior.co[1] * (1 + (tau - 3) * u*u + (2 - tau) *u*u*u)
             pos3 = kfrm_posterior.co[1] * (tau * u + (3-2*tau)*u*u + (tau-2)*u*u*u)
             pos4 = kfrm_posterior2.co[1] * (-tau *u*u + tau*u*u*u)
             pos = pos1 + pos2 + pos3 + pos4
             
             break
    return pos       
#end




