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
            self.raiz = aux.siguiente
            del aux
        else:
            print("               \nLa cola esta vacia")
    
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
                break
        print(cadena)