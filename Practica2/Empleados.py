import xml.etree.ElementTree as ET
import os
class Empleado:
    def __init__(self, root = None, arbol = None):
        self.root = root
        self.arbol = arbol

    def verEmpleado(self, idBuscado):
        
        self.encontrado = False
        
        for departamento in self.root.findall('./departamento'):
            
            for empleado in departamento.findall('./empleado'):

                self.id = int(empleado.get('id'))

                if self.id == idBuscado:
                    print("el id si coincide")
                    self.nombre = empleado.find('./nombre').text
                    self.puesto = empleado.find('./puesto').text
                    self.salario = empleado.find('./salario').text
                    print()
                    print("id: ", self.id, " nombre: ", self.nombre," puesto: ", self.puesto, " salario: ", self.salario)

                    self.encontrado = True
        
        if self.encontrado == False:
            print("\n                El empleado no existe")

    def modificarEmpleado(self, idBuscado):
        
        
        for departamento in self.root.findall('./departamento'):

            for empleado in departamento.findall('./empleado'):

                self.id = int(empleado.get('id'))

                if idBuscado == self.id:
                    nombre = input("Ingrese nuevo nombre: ")
                    empleado.find('nombre').text = nombre

                    puesto = input("Ingrese nuevo puesto: ")
                    empleado.find('puesto').text = puesto

                    salario = input("Ingrese nuevo salario: ")
                    empleado.find('salario').text = salario

        #self.arbol.write('empleados.xml')

    def eliminarEmpleado(self, idBuscado):
        
        for departamento in self.root.findall('./departamento'):

            for empleado in departamento.findall('./empleado'):

                self.id = int(empleado.get('id'))

                if idBuscado == self.id:
                    
                    departamento.remove(empleado)
        
        #self.arbol.write('empleados.xml')

    def verTodo(self):
        
        for departamento in self.root.findall('./departamento'):

            dept = departamento.get('departamento')    
            print("Departamento: ", dept)

            for empleado in departamento.findall('./empleado'):
                
                self.id = empleado.get('id')
                self.nombre = empleado.find('./nombre').text
                self.puesto = empleado.find('./puesto').text
                self.salario = empleado.find('./salario').text

                print("\tId: ", self.id)
                print("\t\tnombre: ", self.nombre)
                print("\t\tpuesto: ", self.puesto)
                print("\t\tsalario: ", self.salario)



    def generarArchivo(self):
        self.arbol.write('empleados.xml')

    def graficar(self):
        grafo = 'digraph T{ \nnode[shape=box fontname="Arial" fillcolor="white" style=filled ]'
        grafo += '\nroot[label = \"Empresa\", constraint=false, group=1];\n'
        
        contador = 0
        for departamento in self.root.findall('./departamento'):
            contador += 1
            self.dept = departamento.get('departamento') 
            grafo += '\ndepartamento{}[label = \"departamento: {} \", group="{}"];\n'.format(contador, self.dept, contador)
            
            grafo += '\nroot -> departamento{};'.format(contador)
              

            for empleado in departamento.findall('./empleado'):
                
                self.id = empleado.get('id')
                self.nombre = empleado.find('./nombre').text
                self.puesto = empleado.find('./puesto').text
                self.salario = empleado.find('./salario').text
                
                
                #print("el nombre es: ", self.nombre)
                self.id = self.id.replace("\"", "\\\"")
                self.nombre = self.nombre.replace("\"", "\\\"")
                self.puesto = self.puesto.replace("\"", "\\\"")
                self.salario = self.salario.replace("\"", "\\\"")
                
    
                grafo += '\nempleado{}[label = \"empleado: {}\", group="{}"];\n'.format(self.id, self.id, self.id)
                #grafo += '\nid{}[label = \"id: {}\", group="{}"];\n'.format(self.id, self.id, self.id)
                grafo += '\nnombre{}[label =\"nombre: {}\", group="{}"];\n'.format(self.id, self.nombre, self.id)
                grafo += '\npuesto{}[label = \"puesto: {}\", group="{}"];\n'.format(self.id, self.puesto, self.id)
                grafo += '\nsalario{}[label = \"salario: {}\", group="{}"];\n'.format(self.id, self.salario, self.id)

                grafo += '\ndepartamento{} -> empleado{};'.format(contador, self.id )
                #grafo += '\nempleado{} -> id{};'.format(self.id, self.id )
                grafo += '\nempleado{}-> nombre{};'.format(self.id, self.id)
                grafo += '\nempleado{}-> puesto{};'.format(self.id, self.id)
                grafo += '\nempleado{} -> salario{};'.format(self.id, self.id)




        grafo += '}'

        # ---- luego de crear el contenido del Dot, procedemos a colocarlo en un archivo
        dot = "{}_dot.txt".format('empleados')
        with open(dot, 'w') as f:
            f.write(grafo)
        result = "{}.png".format('empleados')
        os.system("dot -Tpng " + dot + " -o " + result)