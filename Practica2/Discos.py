from this import s


class Disco:
    def __init__(self, root = None, arbol = None):
        self.root = root
        self.arbol = arbol

    def verDisco(self, titulo):
        
        self.encontrado = False

        for elemento in self.root.findall('./cd'):           
            
            self.title = elemento.find('./title').text
            
            if self.title == titulo:
                self.encontrado = True

                self.artist = elemento.find('./artist').text
                self.country = elemento.find('./country').text
                self.company = elemento.find('./company').text
                self.price = elemento.find('./price').text
                self.year = int(elemento.find('./year').text)

                print("Title: ", self.title, " artist: ", self.artist, " country: ", self.country, " company: ", self.company,
                " price: ", self.price, " year: ", self.year)
        
        if self.encontrado == False:
            print("\n             El disco no existe")

    def modificarDisco(self, titulo_Buscado):

        for elemento in self.root.findall('./cd'):
            titulo = elemento.find('./title').text

            if titulo == titulo_Buscado:
                artista = input("Ingrese nuevo artista: ")
                pais = input("Ingrese nuevo pais: ")
                compania = input("Ingrese nueva compania: ")
                precio = input("Ingrese nuevo precio: ")
                year = input("Ingrese nuevo año: ")

                elemento.find('./artist').text = artista
                elemento.find('./country').text = pais
                elemento.find('./company').text = compania
                elemento.find('./price').text = precio
                elemento.find('./year').text = year
        
        #self.arbol.write('discos.xml')
    
    def eliminarDisco(self, titulo_buscado):

        for elemento in self.root.findall('./cd'):
            titulo = elemento.find('./title').text

            if titulo == titulo_buscado:
                
                self.root.remove(elemento)

        #self.arbol.write('discos.xml')

    def verTodo(self):

        for elemento in self.root.findall('./cd'):
            titulo = elemento.find('./title').text
            artista = elemento.find('./artist').text 
            pais = elemento.find('./country').text
            compania = elemento.find('./company').text
            precio = elemento.find('./price').text
            anio = elemento.find('./year').text

            print("titulo: ", titulo, 
            "\n\tartista: ", artista,
            "\n\tpais: ", pais,
            "\n\tcompania: ", compania,
            "\n\tprecio: ", precio,
            "\n\taño: ", anio)


    def generarArchivo(self):
        self.arbol.write('discos.xml')
