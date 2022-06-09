class NodoCarritos:
    def __init__(self, valor = None, siguiente = None):
        self.valor = valor
        self.siguiente = siguiente


class Carritos:
    def __init__(self):
        self.raiz = NodoCarritos()
        self.ultimo = NodoCarritos()
        
    def apilar(self, nuevoNodo):
        
        if self.raiz.valor is None:
            self.raiz = nuevoNodo
            self.ultimo = nuevoNodo
            
        elif self.raiz.siguiente is None:
            self.raiz.siguiente = nuevoNodo
            self.ultimo = nuevoNodo
        else:
            self.ultimo.siguiente = nuevoNodo
            self.ultimo = nuevoNodo

    def desapilar(self, carrito = None):
        if carrito is None:
            if self.raiz.siguiente is None:
                self.raiz = NodoCarritos()
            else:
                nodoaux = self.raiz
                nodoPenultimo = nodoaux
                
                while nodoaux.siguiente is not None:
                    nodoPenultimo = nodoaux
                    nodoaux = nodoaux.siguiente
                
                nodoPenultimo.siguiente = None
        else:
            if self.raiz.valor is carrito:
                if self.raiz.siguiente is not None:
                    self.raiz = self.raiz.siguiente
                else:
                    self.raiz = NodoCarritos()
            else:
                nodoaux = self.raiz
                nodoAnterior = nodoaux
                
                while nodoaux.valor is not carrito:
                    nodoAnterior = nodoaux
                    nodoaux = nodoaux.siguiente
                    
                nodoAnterior.siguiente = nodoaux.siguiente
    
    def getNodoPila(self, carrito = None): 
        if carrito is None:
            if self.raiz.siguiente is None:
                return self.raiz.valor
            else:
                nodoaux = self.raiz
                nodoPenultimo = nodoaux
                
                while nodoaux.siguiente is not None:
                    nodoPenultimo = nodoaux
                    nodoaux = nodoaux.siguiente
                
                return nodoaux.valor
    
    def recorrerPila(self):
        nodoAux = self.raiz
        
        cadena = ''
        while True:
            if nodoAux is not None:
                cadena += '(' + str(nodoAux.valor) + ') -> '
                if nodoAux.siguiente is not None:
                    nodoAux = nodoAux.siguiente
                else:
                    break
            else:
                break
        print(cadena)