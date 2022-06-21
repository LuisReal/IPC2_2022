import xml.etree.ElementTree as ET

class Disco:
    def __init__(self, root = None, arbol = None):
        self.root = root
        self.arbol = arbol

    def verDisco(self):

        self.doc = ET.parse('Tarea4/discos.xml')
        self.root = self.doc.getroot()
        
        self.encontrado = False

        self.buscar = int(input("Ingrese el año a buscar: "))

        for elemento in self.root.findall('./cd'):           
            
            self.year = int(elemento.find('./year').text)
            
            if self.year == self.buscar:
                self.encontrado = True

                self.title = elemento.find('./title').text
                self.artist = elemento.find('./artist').text
                self.country = elemento.find('./country').text
                self.company = elemento.find('./company').text
                self.price = elemento.find('./price').text
               

                print("Title: ", self.title, " artist: ", self.artist, " country: ", self.country, " company: ", self.company,
                " price: ", self.price, " year: ", self.year)
        
        if self.encontrado == False:
            print("\n             El disco no existe")

disco = Disco()

disco.verDisco()