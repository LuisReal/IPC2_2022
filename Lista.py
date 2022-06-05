class NodoLista:
    def __init__(self, id= None, nombre=None, carrito=None, siguiente = None):
        self.id = id
        self.nombre = nombre
        self.carrito = carrito
        self.siguiente = siguiente
    
class Lista():
    def __init__(self) -> None:
        self.raiz = NodoLista()
        self.ultimo = NodoLista()

    def insertar(self, nodoNuevo):
        if self.raiz.id is None:
            self.raiz =  nodoNuevo
        elif self.raiz.siguiente is None:
            self.raiz.siguiente = nodoNuevo
            self.ultimo = nodoNuevo
        else:
            self.ultimo.siguiente = nodoNuevo
            self.ultimo = nodoNuevo
    
    def recorrerLista(self):
        actual = self.raiz

        cadena = ''
        while True:
            if actual.nombre is not None:
                cadena += "id: " + str(actual.id)  +" nombre: "+actual.nombre + " carrito: "+ str(actual.carrito)
                if actual.siguiente is not None:
                    cadena += "\n"
                    actual =  actual.siguiente
                else:
                    break
            else:
                break
        print(cadena)
    
    def buscarCliente(self, id):
        actual = self.raiz

        while actual.id != id:
            if actual.siguiente is not None:
                actual = actual.siguiente
            else:
                return None
        
        return actual
    
    def eliminarCliente(self, id):
        actual = self.raiz
        anterior = None

        while actual and actual.id != id:
            anterior = actual
            actual = actual.siguiente

        if anterior is None:
            self.raiz = actual.siguiente
            actual.siguiente = None
        elif actual:
            anterior.siguiente = actual.siguiente
            actual.siguiente = None