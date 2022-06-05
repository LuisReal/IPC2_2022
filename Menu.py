from Pila import Carritos, NodoCarritos
from Lista import NodoLista, Lista
class Menu:
    def __init__(self) -> None:
    
        opc = 0
        self.id = 0
        self.lista = Lista()
        self.pila = Carritos()

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
                    self.lista.insertar(NodoLista(self.id, nombre, carrito))
                    self.pila.desapilar()

                self.lista.recorrerLista()

            
            elif opc == 3:
                cliente = int(input("Ingrese el id del cliente a seleccionar: "))

                nodo = self.lista.buscarCliente(cliente)

                print("Nombre: ", nodo.nombre, " Carrito: ", nodo.carrito)

                respuesta = 0

                while respuesta <2:
                    print("1. Pagar\n"
                    , "2. Regresar")
                    respuesta = int(input("Ingrese opcion: "))
                    
                    if  respuesta == 1:
                        print("pagando...")

                        self.lista.eliminarCliente(cliente)
                        print("Se elimino el cliente ", cliente, "\n")
                        self.lista.recorrerLista()
                    elif respuesta == 2:
                        print("           regresando....")
                    
            
            elif opc == 4:
                print("Caja Registradora")
            
            elif opc == 5:
                print("Visualizar Datos")
            
            else:
                print("saliendo.....")

menu = Menu()