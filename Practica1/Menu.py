from Pila import Carritos, NodoCarritos
from Lista import Lista, NodoLista
from Cola import Cola , NodoCola

class Menu:
    def __init__(self) -> None:
    
        opc = 0
        self.id = 0
        self.lista = Lista()
        self.pila = Carritos()
        self.cola = Cola()

        while opc<6:

            print("Menu Principal \n",
            "1. Ingreso de datos\n",
            "2. Nuevo Cliente\n",
            "3. Ver Cliente\n",
            "4. Caja Registradora\n",
            "5. Visualizar Datos\n")
            
            opc = int(input("Ingrese una opcion a elegir: "))

            if opc == 1:
                
                carritos = int(input("Ingrese cantidad de carritos: "))

                if carritos <0 :
                    print("\n                   No se aceptan numeros negativos")
                else:
                    for a in range(carritos):
                        self.pila.apilar(NodoCarritos(a+1))

                self.pila.recorrerPila()
        
            elif opc == 2:
                nombre = input("Ingrese el nombre del cliente: ")
                self.id = self.id+1
                carrito = self.pila.getNodoPila()
                

                if carrito is None:
                    print("\n       No hay carritos disponibles, no puede ingresar mas clientes\n")
                else:

                    print("el nodo desapilado(carrito) es: ", carrito)
                    print("self.id: ", self.id)
                    print("nombre: ", nombre)
                    print("carrito: ", carrito)
                    print()
                    self.lista.insertar(NodoLista(self.id, nombre, carrito))
                    self.pila.desapilar()

                self.lista.recorrerLista()

            
            elif opc == 3:
                

                respuesta = 0

                while respuesta <2:
                    cliente = int(input("Ingrese el id del cliente a seleccionar: "))
                    nodo = self.lista.buscarCliente(cliente)
                    
                    if nodo is None:
                        print("           No existe el cliente seleccionado")
                        break
                    else:
                        print("id: ", nodo.id ,"Nombre: ", nodo.nombre, " Carrito: ", nodo.carrito)
                        print("1. Pagar\n"
                        , "2. Regresar")
                        respuesta = int(input("Ingrese opcion: "))
                        
                        if  respuesta == 1:
                            print("pagando...")
                            
                            self.cola.insertar(NodoCola(nodo))
                            self.lista.eliminarCliente(cliente)
                            
                            print("Se elimino el cliente ", cliente, "\n")
                            
                            self.lista.recorrerLista()

                            vacia = self.lista.lista_vacia()
                            if vacia == None:
                                break

                        elif respuesta == 2:
                            print("           regresando....")
                        
            
            elif opc == 4:
                print("Caja Registradora")
                self.cola.recorrerCola()
                
                opc = 0
                while(opc < 2):
                    print("1. Avanzar\n",
                    "2. Regresar")

                    opc = int(input("Ingrese opcion: "))

                    if opc == 1:
                        self.cola.desencolar()
                        nodo_eliminado = self.cola.getNodoEliminado()
                        #print("Carrito eliminado: ", nodo_eliminado.valor.carrito)
                        if nodo_eliminado == None:
                            print("No existen mas carritos en la cola de la caja")
                        else:
                            self.pila.apilar(NodoCarritos(nodo_eliminado.valor.carrito))
                        self.cola.recorrerCola()
                        #self.pila.recorrerPila()
                    else:
                        print("Regresando")
                   
                        

            elif opc == 5:
                print("                 Pila de Carritos\n")
                self.pila.recorrerPila()
                print("\n               Lista de Clientes\n")
                self.lista.recorrerLista()
                print("\n               Cola Caja Registradora\n")
                self.cola.recorrerCola()
            
            else:
                print("saliendo.....")

menu = Menu()