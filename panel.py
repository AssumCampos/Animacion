# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:57:02 2020

@author: Ana López Díez
Maria Assumpció Campos Martínez
Antonio José Lara Buenrostro
Lucía Medina Gómez
"""

#Importamos las bibliotecas necesarias y utilizamos la funcion reload para 
#poder utilizar el main con el panel

from importlib import reload
import bpy

import main 
reload(main)

import insertar_fotogramas 
reload(insertar_fotogramas)


"""
Clase en la que creamos los elementos que vamos a modificar desde el panel
Para cada valor, especificamos que nombre usar y un valor por defecto.
Si es necesario, se añade un valor minimo, ya sea para un entero o para un decimal
"""

class AnimSettings(bpy.types.PropertyGroup):
    #Numero de copias que deseamos implementar en la interpolacion. Por defecto 0, valor minimo 0.
    copias= bpy.props.IntProperty(name= "Numero de copias", default=1, min=1)

    #Desplegable donde podemos elegir el metodo de interpolacion: lineal, Hermite o Catmull-Rom. Por defecto Lineal.
    my_enum= bpy.props.EnumProperty(name= "metodo", description= "metodo_a_elegir", items= [('lineal', "Lineal", ""), ('hermite', "Hermite", ""),  ('catmullrom', "Catmull-Rom", "")] )

    #Checkbox para seleccionar si queremos que nuestra interpolacion tenga una oscilacion aleatoria. Por defecto, True (si queremos).
    my_bool = bpy.props.BoolProperty(name="Oscilacion aleatoria", description="oscilacion_al", default = False)

    #Amplitud de la oscilacion aleatoria. Por defecto 0.0, valor minimo 0.
    my_amplitud = bpy.props.FloatProperty(name= "Amplitud maxima", default= 0.0, min=0)

    #Tension utilizada cuando se selecciona Catmull-Rom. Por defecto 0.0, valor minimo 0
    my_tau = bpy.props.FloatProperty(name= "Tension(tau)", default= 0.0, min=0)

    #Frecuencia con la que se insertaran los keyframes interpolados. Por defecto 5, valor minimo 0
    my_frecuencia = bpy.props.IntProperty(name= "Frecuencia", default= 5, min=0)

    #Desplegable donde podemos elegir el metodo de interpolacion: lineal, Hermite o Catmull-Rom. Por defecto Lineal.
    my_tipoVelocidad = bpy.props.EnumProperty(name= "Elegir velocidad", description= "Elegir velocidad", items= [('velDefecto', "Velocidad por defecto", ""),('velCON', "Velocidad Controlada", ""), ('velCTE', "Velocidad constante", "") ] )
    
    #Velocidad a la que irá nuestro objeto
    my_vel = bpy.props.IntProperty(name= "Velocidad", default= 1, min=1)
    
    #Distancia recorrida por el objeto
    distancia_actual = bpy.props.FloatProperty(name= "Distancia", default= 0.0, min=0)
    
    eje_inclinacion = bpy.props.EnumProperty(name= "Elegir eje inclinacion", description= "Elegir eje inclinacion", items= [('ejeX+', "Eje x positivo", ""),('ejeX-', "Eje x negativo", ""), ('ejeY+', "Eje y positivo", ""), ('ejeY-', "Eje y negativo", ""), ('ejeZ+', "Eje z positivo", ""), ('ejeZ-', "Eje z negativo", "") ] )
    
    eje_lateral = bpy.props.EnumProperty(name= "Elegir eje lateralización", description= "Elegir eje lateral", items= [('ejeX+', "Eje x positivo", ""),('ejeX-', "Eje x negativo", ""), ('ejeY+', "Eje y positivo", ""), ('ejeY-', "Eje y negativo", ""), ('ejeZ+', "Eje z positivo", ""), ('ejeZ-', "Eje z negativo", "") ] )

    #Checkbox para seleccionar si queremos que nuestra interpolacion tenga una oscilacion aleatoria. Por defecto, True (si queremos).
    inclinacion_bool = bpy.props.BoolProperty(name="Inclinación", description="inclinacion", default = False)
    
    #Distancia recorrida por el objeto
    inclinacion = bpy.props.FloatProperty(name= "Inclinacion", default= 0.0)
    
    
"""
Creacion de un operador donde podemos seleccionar el metodo de interpolacion
y que al darle al boton de interpolar nos ejecute el main con los valores
seleccionados
"""

class elegirMetodo(bpy.types.Operator):
    """Interpolamos la trayectoria"""
    #ID con el que identificamos que queremos que seleccione en nuestro main
    bl_idname = "object.interpolar_valores"

    #Etiqueta que aparecera en el panel
    bl_label = "metodo"

    @classmethod
    def poll(cls, context):
        """
        Funcion que verifica si la escena tiene un objeto activo, si tiene datos de animación,
        si tiene acciones esos datos de animación y si están en los tres ejes los keyframes.

        Parameters
        ----------
        cls :
        context : bpy.context
            Area en la que estamos accediendo con Blender.

        Returns
        -------
        Boolean
            Devolvera True si tiene un objeto activo, con animación 
            y acción en esa animación y keyframes en los tres ejes 
            y False si no existe.

        """
        encontrado = False
        obj = context.active_object
        if obj is not None :
            ad = obj.animation_data
            if ad is not None:
                act = ad.action
                if act is not None:
                    cx = act.fcurves.find('location',index=0)
                    cy = act.fcurves.find('location',index=1)
                    cz = act.fcurves.find('location',index=2)
                    if cx and cy and cz: # si alguno es None devuelve False
                        encontrado = True
        
        return encontrado

    def execute(self, context):
        """
        Funcion que ejecuta el main una vez pulsado el boton "interpolar"

        Parameters
        ----------
        context : bpy.context
            Area en la que estamos accediendo con Blender.

        Returns
        -------
        set
            Devuelve que se ha realizado la ejecucion.

        """  
        # Generamos la tabla de frames con su distancia
        tabla = insertar_fotogramas.generar_tabla()
        print(f"Longitud tabla: {len(tabla)}")
        main.main(tabla)
        return {'FINISHED'}   


"""
Creación de un nuevo operador para eliminar todas las copias
que se hacen del objeto en cada interpolacion
"""

class eliminarCopias(bpy.types.Operator):
    """Eliminamos las copias"""
    bl_idname = "object.elimina_copias"
    bl_label = "eliminar"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        i = len(bpy.data.collections) - 1
    
        while i >= 0:
            if bpy.data.collections[i].name[0:9] == "Copias de" :
                bpy.data.collections.remove(bpy.data.collections[i])
            i = i-1
        
        
        return {'FINISHED'}  

"""
Creacion del panel en el que se añaden los operadores y elementos creados
"""
class AnimPanel(bpy.types.Panel):

    #Nombre del panel
    bl_label = "Propiedades interpolacion"
    
    #ID con el que se reconoce el panel
    bl_idname = "OBJECT_PT_hello"
    
    #Panel de edicion en el que aparecera el panel
    bl_space_type = 'PROPERTIES'
    
    #Espacio de Blender en el que aparecera el panel
    bl_region_type = 'WINDOW'
    
    #Pestaña de la seccion de propiedades en la que aparecera el panel
    bl_context = "object"

    def draw(self, context):
        """
        Parameters
        ----------
        context : bpy.context
            Area en la que estamos accediendo con Blender.

        Returns
        -------
        None.

        """
        
        layout = self.layout.column(align = True)
        
        layout = self.layout

        #Puntero al objeto activo
        obj = context.object

        #Insertamos el desplegable creado con anterioridad
        layout.prop(obj.AnimSettings, "my_enum")
        
        if bpy.context.object.AnimSettings.my_enum == 'catmullrom':
            #Si seleccionamos catmull, nos aparecera la opcion de modificar tau
            layout.prop(obj.AnimSettings, "my_tau")
        
        #Elegimos qué velocidad queremos
        layout.prop(obj.AnimSettings, "my_tipoVelocidad")
        
        #Si en my ejercicio elegimos velocidad por defecto entonces añadiremos la frecuencia
        if bpy.context.object.AnimSettings.my_tipoVelocidad == 'velDefecto': 
            layout.prop(obj.AnimSettings, "my_frecuencia")
        #Si en my ejercicio elegimos velocidad constante entonces añadiremos la velocidad
        elif bpy.context.object.AnimSettings.my_tipoVelocidad == 'velCTE': 
            layout.prop(obj.AnimSettings, "my_vel")
        #Si en my ejercicio elegimos velocidad controlada entonces añadiremos la distancia   
        elif bpy.context.object.AnimSettings.my_tipoVelocidad == 'velCON':
            layout.prop(obj.AnimSettings, "distancia_actual")
            
        #Insertamos el valor de copias al panel para poder ser modificado
        layout.prop(obj.AnimSettings, "copias")
                
        #Insertamos el checkbox usado para la oscilacion
        layout.prop(obj.AnimSettings, "my_bool")
        
        if bpy.context.object.AnimSettings.my_bool == True:
            #Si esta seleccionado, aparece la opcion para modificar la amplitud
            layout.prop(obj.AnimSettings, "my_amplitud")
        
        layout.prop(obj.AnimSettings, "eje_inclinacion")
        layout.prop(obj.AnimSettings, "eje_lateral")
        
        layout.prop(obj.AnimSettings, "inclinacion_bool")
        if bpy.context.object.AnimSettings.inclinacion_bool == True:
            layout.prop(obj.AnimSettings, "inclinacion")
            
        #Boton con el que llamamos al operador creado y añadimos una etiqueta
        #visible en Blender
        layout.operator("object.interpolar_valores", text = "interpolar")
        
        layout.operator("object.elimina_copias", text = "Eliminar Copias")
                           
def register():
    """
    Registra las propiedades, operadores y paneles para poder usarlos en Blender

    Returns
    -------
    None.

    """
    bpy.utils.register_class(AnimSettings)
    bpy.types.Object.AnimSettings = bpy.props.PointerProperty(type= AnimSettings)
    bpy.utils.register_class(elegirMetodo)
    bpy.utils.register_class(eliminarCopias)
    bpy.utils.register_class(AnimPanel)
    

def unregister():
    """
    Elimina lo registrado en la funcion anterior

    Returns
    -------
    None.

    """
    bpy.utils.unregister_class(AnimSettings)
    bpy.utils.unregister_class(elegirMetodo)
    bpy.utils.unregister_class(eliminarCopias)
    bpy.utils.unregister_class(AnimPanel)


if __name__ == "__main__":
    register()
