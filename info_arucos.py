


dict_arucos = {

    #El diccionario esta construido de la siguiente manera:
    # id_Aruco : [TIPO, SUBTIPO, ORDEN, INFO ADICIONAL, INFO SALIDA]

    # TIPO: Puede ser E (Entrada), D(Derecha), I(Izquierda), V(Variable (Izq/Der)), F(Fancy)

    # SUBTIPO: Depende del tipo general para la denominacion de este:

    #   Si es TIPO E: Puede tener 4 sub-tipos: "1", "2", "3", que indica la ruta de laberinto a usar. En
    #   caso de ser "R", seguira una ruta random.
    #   Si es TIPO D: Solo tiene sub-tipo "S" si es aruco de salida.
    #   Si es TIPO I: Solo tiene sub-tipo "S" si es aruco de salida.
    #   Si es TIPO V: No tiene sub-tipo.
    #   Si es TIPO F: Tiene sub-tipo "D" para indicar que es un aruco que indica doblar a la derecha o hacer ruta especial
    #                 Tiene sub-tipo "I" para indicar que es un aruco que indica doblar a la izquierda o hacer ruta especial
    #                 Tiene sub-tipo "V" para indicar que es un aruco que indica doblar a la izquierda/derecha o hacer ruta especial
    #                 Tiene sub-tipo "R" para indicar que es un aruco de callejon sin salida y debe retroceder(girar en 180º)
    #                 Tiene sub-tipo "S" para indicar que es un aruco que indica salir del laberinto o hacer ruta especial

    # ORDEN: Solo presente en los arucos del tipo Variable y Fancy. Es una lista del tipo [a,b,c] en donde se indica el orden segun
    # la ruta del laberinto usada. Por ejemplo, si se tiene un aruco que para la ruta 1 y 2 del laberinto, la omni debe girar hacia
    # la izquierda, mientras que en la ruta 3 hacia la derecha, esta lista se construirá asi: ["I", "I", "D"]



    0 :   ["E", "R" , None            ,None], 
    1 :   ["E", "1" , None            ,None], 
    2 :   ["E", "2" , None            ,None], 
    3 :   ["E", "3" , None            ,None], 
    100 : ["D", None, None            ,None],
    200 : ["I", None, None            ,None],
    301 : ["V", None, ["I" ,None,"D"]  ,None],
    302 : ["V", None, [None,None,None],None],
    303 : ["V", None, [None,"D","I"]  ,None],
    304 : ["V", None, ["D" ,"I","D"]   ,None],
    305 : ["V", None, ["I" ,None,"D"]  ,None],
    306 : ["V", None, [None,"I","D"]  ,None],
    307 : ["V", None, ["D" ,"D","I"]   ,None],
    308 : ["V", None, [None,None,"D"] ,None],
    309 : ["V", None, [None,"I",None] ,None],
    401 : ["F", "I" , ["I" ,"",""]     ,None],
    402 : ["F", "R" , [None,None,None],None],
    403 : ["F", "R" , [None,None,None],None],
    404 : ["F", "I" , [None,"",""]    ,None],
    405 : ["F", "V" , [None,"",""]    ,None],
    406 : ["F", "V" , ["I","",""]     ,None],
    407 : ["F", "V" , [None,"",""]    ,None],
    408 : ["F", "I" , ["I" ,"",""]     ,None],
    409 : ["F", "I" , [None,"",""]    ,None],
    410 : ["F", "I" , [None,"",""]    ,None],
    411 : ["F", "S" , [None,None,None],None],
    412 : ["F", "S" , [None,None,None],None],
    413 : ["F", "S" , [None,None,None],None],


    

}
























class Aru():
    def __init__(self,id):
        self.aru = None #El aruco 
        self.type = None #Tipo de Aruco : "E"(Entrada); "I"(Izquierda); "D"(Derecha); "S"(Sin Salida); "V"(Variable); "F"(Fancy)
        self.left = None #Cuánto avanza hacia la izquierda
        self.right = None #Cuánto avanza hacia la derecha
        self.back = None #Cuánto avanza hacia atras
        self.dec = None #Variable de decision, que determina que camino seguir para aruco -1(I), 1(D), 0(Opción Fancy)

    def tipoAr(self, tipo):
        self.type = tipo

    def decision(self, dec):
        self.dec = dec

    def izq(self, dist):
        self.left = dist

    def der(self, dist):
        self.right = dist

    def retro(self, dist):
        self.back = dist













    def orden(self):

        #Cuando se tiene que ir a la izquierda
        if self.type == "I" or (self.type == "V" and self.dec == -1) or (self.type == "F" and self.dec == -1):
            return [90, self.left]
        
        #Cuando se tiene que ir a la derecha
        if self.type == "D" or (self.type == "V" and self.dec == 1) or (self.type == "F" and self.dec == 1):
            return [-90, self.right]
        
        #Cuando se tiene que retroceder
        if self.type == "S":
            return [180, self.back]
        
        #Cuando se tiene una version fancy que no es izq ni der
        if self.type == "F" and self.dec == 0:
            return [0,0]





    