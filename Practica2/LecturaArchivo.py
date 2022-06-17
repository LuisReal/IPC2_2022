import xml.etree.ElementTree as ET


class Archivo:
    def __init__(self):
        self.root_discos = ""
        self.root_empleados = ""
        self.doc_empleados = ""

    def lecturaDiscos(self, ruta):    
        self.doc_discos = ET.parse(ruta) #xmlfile contiene la ruta del archivo y se procesa
        self.root_discos = self.doc_discos.getroot()

        
    def lecturaEmpleados(self, ruta):
        self.doc_empleados = ET.parse(ruta)
        self.root_empleados = self.doc_empleados.getroot()

        
        
        
        

        

    

                



                
                

            