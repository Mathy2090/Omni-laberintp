from controlClient import ControlClient
from streamClient import StreamClient
from aruco_huntingv2 import *
from info_arucos import dict_arucos
import cv2
import time
import math
import random


ip = "172.20.10.10"
camara = StreamClient(ip)
#control = ControlClient(ip, 12345)

#Reconocimiento del id del aruco, y parametros camara + aruco
hunter = ArucoHunting() 
camera_matrix = np.array([[465.,0. , 302.],[0., 451., 246.], [0., 0., 1.]])
hunter.set_marker_length(0.07) # Dado por cubo simulado
hunter.set_camera_parameters(camera_matrix) # Matriz de la cámara

#Calibra mas aun la posicion del aruco para tener asi mas precision
def calib(posAruco):

    y = posAruco[2]
    yAjustado = -0.4135*(y**2) + 1.3892*y - 0.019
    
    return [posAruco[0],yAjustado,posAruco[1]]

#Retorna los id del aruco que procesa.
def get_Aruco(img):
    global hunter
    hunter.update_image(img) #Se actualiza la imagen del detector
    hunter.update_pose_and_ids() #Se recolecta la pose detectada
    arucos_data = hunter.arucos_data # Ejecutar aruco_huntingv2.py y llamar esa 
    #print(arucos_data)
    
    if arucos_data != []:

        id_arucos_encontrados = []
        for data in arucos_data:
            idAruco = data["id"]
            posAruco = data["position"]
            orAruco = data["orientation"]
            posArucoCalibrada = calib(posAruco)
            id_arucos_encontrados.append([idAruco,posArucoCalibrada,orAruco])
            print("ID:"+str(idAruco)+"|||x:"+ str(posArucoCalibrada[0]) + "  y:"+ str(posArucoCalibrada[1])+ "  z:"+ str(posArucoCalibrada[2]))
            
        return id_arucos_encontrados

    #Si no encontro aruco, retorna None.
    else:
        return None
    

#Recibe la instruccion a realizar y la traduce al string que recibe controlClient    
def instuccionSTR(x,y,grad):
    angulo = math.radians(grad)
    angulo = ((angulo*1000)//1)/1000

    stringInstr = "x:" + str(x) + ",y:" + str(y) + ",o:" + str(angulo) + ",dt:0.1,t_max:1"
    
    return stringInstr

# #Recibe el id y el camino configurado del laberinto (si sigue el camino 1, 2, 3 o random)
# def accionOmni(id, camino="R"):
#     global control
#     global resuelto

#     data = dict_arucos[id]
#     tipo = data[0]
#     subtipo = data[1]
#     orden = data[2]
#     infoFancy = data[3]

#     #Si es aruco Derecha, se rota
#     if tipo == "D":
#         rot = instuccionSTR(0,0,-90)
#         control.send(rot)
#         return 
    
#     #Si es aruco Izquierda, se rota
#     elif tipo == "I":
#         rot = instuccionSTR(0,0,90)
#         control.send(rot)
#         return
    
#     #Si es aruco Variable, se rota dependiendo del caso d config.
#     elif tipo == "V":

#         #Se debe analizar en que tipo de camino se esta
#         if camino == "1":
#             posViraje = orden[1]
          
#         elif camino == "2":
#             posViraje = orden[2]
        
#         elif camino == "3":
#             posViraje = orden[3]

#         elif camino == "R":
#             alAzarA = random.randint(1,2)
            
#             #Lo hacemos al azar la eleccion de si es a la izquierda o derecha.
#             if alAzarA == 1:
#                 posViraje = "D"
#             else:
#                 posViraje = "I"
        
#         if posViraje == "D":
#             rot = instuccionSTR(0,0,-90)

#         elif posViraje == "I":
#             rot = instuccionSTR(0,0,90)
    
#         control.send(rot)
#         return

#     #Si el aruco es de tipo Fancy quiere decir que hara un movimiento especifico, se deben analizar los subtipos.
#     elif tipo == "F":

#         #Se vera el subtipo en primer momento, si es de salida, se saldra con la instruccion guardada en infoFancy
#         if subtipo == "S":

#             #Se leen las instrucciones
#             rot = instuccionSTR(0,0,infoFancy[0])
#             tras = instuccionSTR(0,infoFancy[1],0)

#             #Se entregan las instrucciones
#             control.send(rot)
#             control.send(tras)

#             #Se resuelve el problema por lo que la variable global resuelto pasa a ser True.
#             resuelto = True
#             return
        
#         #El otro subtipo es donde debe retroceder, ya que llego a un camino sin salida
#         elif subtipo == "R":

#             #Se leen y entregan las instrucciones
#             rot = instuccionSTR(0,0,infoFancy[0])
#             control.send(rot)
#             return
        
#         #En el caso de los subtipos I, D, V
#         else:
        
#             #Ahora bien, dependiendo del camino, existen opciones que el aruco puede tomar. Si el camino no
#             # es random, entonces solo existe una opcion, que esta guardada en orden. Analizaremos los casos
#             # para cuando no es random.
#             #Si el subtipo es I, quiere decir que puede hacer la instruccion de ir a la izquierda o realizar
#             # el camino "Fancy"
#             if camino != "R":
#                 #Analizamos el camino y el tipo de orden.
#                 if camino == "1":
#                     ordenARealizar = orden[1]
                
#                 elif camino == "2":
#                     ordenARealizar = orden[2]
                
#                 elif camino == "3":
#                     ordenARealizar = orden[3]

#                 #Realizamos la orden pedida
#                 if ordenARealizar== "D":
#                     rot = instuccionSTR(0,0,-90)
#                     control.send(rot)
#                     return

#                 elif ordenARealizar == "I":
#                     rot = instuccionSTR(0,0,90)
#                     control.send(rot)
#                     return
                
#                 #En el caso de que la orden a realizar es una "Fancy"
#                 elif ordenARealizar == "F":

#                     #Se leen las instrucciones
#                     rot1 = instuccionSTR(0,0,infoFancy[0])
#                     tras1 = instuccionSTR(0,infoFancy[1],0)
#                     rot2 = instuccionSTR(0,0,infoFancy[2])

#                     #Se entregan las instrucciones
#                     control.send(rot1)
#                     control.send(tras1)
#                     control.send(rot2)
#                     return
                
#                 #En el caso de que el camino sea random
#                 else:
#                      #Lo primero se leera el subtipo

#                     if subtipo == "D":
#                         alAzarB = random.randint(1,2)

#                         #Lo hacemos al azar la eleccion de si es a la derecha o camino Fancy.
#                         if alAzarB == 1:
#                             ordenARealizar = "D"
#                         else:
#                             ordenARealizar = "F"
                    
#                     elif subtipo == "I":
#                         alAzarB = random.randint(1,2)

#                         #Lo hacemos al azar la eleccion de si es a la izquierda o camino Fancy.
#                         if alAzarB == 1:
#                             ordenARealizar = "I"
#                         else:
#                             ordenARealizar = "F"
                     
#                     elif subtipo == "V":
#                         alAzarB = random.randint(1,3)

#                         #Lo hacemos al azar la eleccion de si es a la derecha, izquierda o camino Fancy.
#                         if alAzarB == 1:
#                             ordenARealizar = "D"
#                         elif alAzarB == 2:
#                             ordenARealizar = "I"
#                         else:
#                             ordenARealizar = "F"
                    
#                     #Realizamos la orden pedida
#                         if ordenARealizar== "D":
#                             rot = instuccionSTR(0,0,-90)
#                             control.send(rot)
#                             return

#                         elif ordenARealizar == "I":
#                             rot = instuccionSTR(0,0,90)
#                             control.send(rot)
#                             return
                
#                         #En el caso de que la orden a realizar es una "Fancy"
#                         elif ordenARealizar == "F":

#                             #Se leen las instrucciones
#                             rot = instuccionSTR(0,0,infoFancy[0])
#                             tras1 = instuccionSTR(0,infoFancy[1],0)
#                             rot2 = instuccionSTR(0,0,infoFancy[2])

#                             #Se entregan las instrucciones
#                             control.send(rot1)
#                             control.send(tras1)
#                             control.send(rot2)
#                             return


                    






       


# t=0
# while True:
#     msg_rotar = 'x:0.1,y:0.0,o:0.628,dt:0.1,t_max:1'
    
#     #Actualizar imagen de camara cada 0.1 segundo hasta encontrar al menos un aruco
#     if t+0.1 < time.time():
#         img = camara.get_frame()
#         t = time.time()
#         control.send(msg_rotar)

#     id_arucos = get_Aruco(img)

#     #Encontro arucos
#     if id_arucos is not None:

#         if len(id_arucos) > 1:
#                 #Tiene que seguir hacia adelante hasta encontrarse con un solo aruco
#                 msg_adelante = 'x:0.1,y:0.0,o:0.0,dt:0.1,t_max:1'
#                 control.send(msg_adelante)
#         else:
        
#             while True:
#             #dist_aruco = distancia_aruco()



t = 0
k=0
i=0
while True:
    # Actualizar imagen de camara cada 0.1 segundos
    if t + 0.01 < time.time():
    
        # Actualizar imagen de camara
        img_RGB = camara.get_frame()
        t = time.time()

    next_aruco = get_Aruco(img_RGB) # Procesar imagen para obtener siguiente pose del drone
    # if next_aruco is not None:
        
    #     while True:

    #         if t + 0.01 < time.time():
    #             img_RGB = camara.get_frame()
    #             t = time.time()

    #         #if np.linalg.norm(dif) < 0.10:
    #         #    break
    #     k = k+1

    #     if k > 200:
    #         break
    
    # if i > 200:
    #         break
    # i = i+1



camara.closeWebRTC()
#control._disconnect()
