from LecturaArchivo import Archivo
from Empleados import Empleado
from Discos import Disco

class Menu:
    def __init__(self):
        opc = 0
        self.archivo = Archivo()
        self.empleado = Empleado()
        self.disco = Disco()

        while opc <5:
            print("1.Carga de datos",
            "\n2.Gestion de empleados",
            "\n3.Gestion de discos",
            "\n4.Reportes")

            opc = int(input("Ingrese una opcion: "))

            if opc == 1:
                

                #ruta = 'C:\Users\Darkun\Desktop\discos.xml'
                self.archivo.lecturaDiscos('discos.xml')
                self.archivo.lecturaEmpleados('empleados.xml')
                self.empleado.root = self.archivo.root_empleados
                self.empleado.arbol = self.archivo.doc_empleados
                self.disco.root = self.archivo.root_discos
                self.disco.arbol = self.archivo.doc_discos

                print("\n                  Se cargaron los datos exitosamente\n")


            elif opc == 2:
                print("Gestion de empleados")

                opcion = 0

                while opcion < 6:

                    print("\n1.Ver empleado",
                    "\n2.Modificacion",
                    "\n3.Eliminacion",
                    "\n4.Ver todo",
                    "\n5.Generar archivo",
                    "\n6.Regresar")

                    opcion = int(input("Ingrese la opcion: "))

                    if opcion == 1:
                        id = int(input("Ingrese el id del empleado: "))
                        self.empleado.verEmpleado(id)
                        
                    elif opcion == 2:
                        
                        id = int(input("Ingrese id a modificar: "))
                        self.empleado.modificarEmpleado(id)
                    
                    elif opcion == 3:
                        
                        id = int(input("Ingrese el id del empleado que desea eliminar: "))
                        self.empleado.eliminarEmpleado(id)
                    
                    elif opcion == 4:
                        
                        self.empleado.verTodo()
                    
                    elif opcion == 5:
                        
                        self.empleado.generarArchivo()
                   
                    else:
                        print("Regresando....")
            
            elif opc == 3:
                print("Gestion de discos")

                opcion = 0

                while opcion < 6:

                    print("\n1.Ver disco",
                    "\n2.Modificacion",
                    "\n3.Eliminacion",
                    "\n4.Ver todo",
                    "\n5.Generar archivo",
                    "\n6.Regresar")

                    opcion = int(input("Ingrese la opcion: "))

                    if opcion == 1:
                        titulo = input("Ingrese el titulo del disco: ")
                        self.disco.verDisco(titulo)
                   
                    elif opcion == 2:
                        
                        titulo = input("Ingrese el titulo del disco a modificar: ")
                        self.disco.modificarDisco(titulo)
                    
                    elif opcion == 3:
                        
                        titulo = input("Ingrese el titulo del disco a eliminar: ")
                        self.disco.eliminarDisco(titulo)
                    
                    elif opcion == 4:
                        self.disco.verTodo()
                    
                    elif opcion == 5:
                        
                        self.disco.generarArchivo()
                    
                    else:
                        print("Regresando.....")
            
            elif opc == 4:
                print("Reportes")

                opcion = 0

                while opcion < 3:

                    print("1.Reporte de empleados",
                    "\n2.Reporte de discos",
                    "\n3.Regresar")

                    opcion = int(input("Ingrese la opcion: "))

                    if opcion == 1:
                        print("Reporte de empleados")
                        self.empleado.graficar()
                    elif opcion == 2:
                        print("Reporte de discos")
                    else:
                        print("Regresando....")
            else:
                print("Saliendo...")

menu = Menu()