class NodoCola:
    def __init__(self, valor = None, siguiente = None):
        self.valor = valor
        self.siguiente = siguiente

class Cola:
    def __init__(self):
        self.raiz = NodoCola()
        self.ultimo = NodoCola()
        
    def insertar(self, nuevoNodo):
        
        if self.raiz.valor is None:
            self.raiz = nuevoNodo
            self.ultimo = nuevoNodo
            
        elif self.raiz.siguiente is None:
            self.raiz.siguiente = nuevoNodo
            self.ultimo = nuevoNodo
        else:
            self.ultimo.siguiente = nuevoNodo
            self.ultimo = nuevoNodo

    def desencolar(self):
        aux = self.raiz

        if aux is not None:
            self.setNodoEliminado(aux)
            self.raiz = aux.siguiente
            del aux
        else:
            print("               \nLa cola esta vacia")
            self.nodo_eliminado = None

    def setNodoEliminado(self, nodo):
        self.nodo_eliminado = nodo

    def getNodoEliminado(self):
        return self.nodo_eliminado
    
    def recorrerCola(self):
        nodoAux = self.raiz
        
        cadena = ''
        while True:
            if nodoAux is not None:
                cadena += '( id: ' + str(nodoAux.valor.id) + ' Nombre: '+ nodoAux.valor.nombre+' carrito: '+ str(nodoAux.valor.carrito)+') -> '
                if nodoAux.siguiente is not None:
                    nodoAux = nodoAux.siguiente
                else:
                    break
            else:
                print("                  No hay mas elementos en la cola de la Caja Registradora")
                break
        print(cadena)