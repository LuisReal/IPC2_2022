from cgi import print_exception
from this import s
import os

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

        existe = False

        for elemento in self.root.findall('./cd'):
            titulo = elemento.find('./title').text

            if titulo == titulo_Buscado:
                existe = True
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

        if existe == False:
            print("No existe el titulo buscado")
        
        #self.arbol.write('discos.xml')
    
    def eliminarDisco(self, titulo_buscado):

        existe = False

        for elemento in self.root.findall('./cd'):
            titulo = elemento.find('./title').text

            if titulo == titulo_buscado:
                existe = True
                self.root.remove(elemento)

        if existe == False:
            print("No existe el titulo buscado")
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

    def graficar(self):
        grafo = 'digraph T{ \nnode[shape=box fontname="Arial" fillcolor="white" style=filled ]'
        grafo += '\nroot[label = \"Catalog\", constraint=false, group="0"];\n'
        
        contador = 0
        for elemento in self.root.findall('./cd'):
            contador += 1
            titulo = elemento.find('title').text
            artista = elemento.find('./artist').text 
            pais = elemento.find('./country').text
            compania = elemento.find('./company').text
            precio = elemento.find('./price').text
            anio = elemento.find('./year').text

            titulo = titulo.replace("\"", "\\\"")
            artista = artista.replace("\"", "\\\"")
            pais = pais.replace("\"", "\\\"")
            compania = compania.replace("\"", "\\\"")
            precio = precio.replace("\"", "\\\"")
            anio = anio.replace("\"", "\\\"")

            grafo += '\ncd{}[label = \"cd \", group="{}"];\n'.format(contador, contador)
            grafo += '\ntitle{}[label = \"title: {}\", group="{}"];\n'.format(contador, titulo, contador)
            grafo += '\nartist{}[label = \"artist: {} \", group="{}"];\n'.format(contador, artista ,contador)
            grafo += '\ncountry{}[label = \"country: {} \", group="{}"];\n'.format(contador, pais ,contador)
            grafo += '\ncompany{}[label = \"company: {} \", group="{}"];\n'.format(contador, compania ,contador)
            grafo += '\nprice{}[label = \"price: {} \", group="{}"];\n'.format(contador, precio ,contador)
            grafo += '\nyear{}[label = \"year: {} \", group="{}"];\n'.format(contador, anio ,contador)

            grafo += '\nroot -> cd{};'.format(contador)
            grafo += '\ncd{} -> title{};'.format(contador, contador)
            grafo += '\ntitle{} -> artist{};'.format(contador, contador)
            grafo += '\ntitle{} -> country{};'.format(contador, contador)
            grafo += '\ntitle{} -> company{};'.format(contador, contador)
            grafo += '\ntitle{} -> price{};'.format(contador, contador)
            grafo += '\ntitle{} -> year{};'.format(contador, contador)

            


        grafo += '}'

        # ---- luego de crear el contenido del Dot, procedemos a colocarlo en un archivo
        dot = "{}_dot.txt".format('discos')
        with open(dot, 'w', encoding = "utf-8") as f:
            f.write(grafo)
        result = "{}.png".format('discos')
        os.system("dot -Tpng " + dot + " -o " + result)