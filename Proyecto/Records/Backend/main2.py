from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import json
import re
import os
departamento = []
empleado = []
nombres = []
puestos = []
salarios = []


def Entrada():
    global archivo , tree, root, departamento
    tree = ET.parse('empleados.xml')
    root = tree.getroot() 
    dep = ""
    departamento.clear()
    empleado.clear()
    nombres.clear()
    puestos.clear()
    salarios.clear()
    for titulo in root.iter("departamento"):
        auxid=[]
        auxnombre =[]
        auxpuesto = []
        auxsalario = []
        departamento.append(titulo.attrib["departamento"])
        
        dep = titulo.attrib["departamento"]
     
        for emp in titulo.iter("empleado"):
            auxid.append(emp.attrib["id"])
            for nombre in emp.iter("nombre"):
                auxnombre.append(nombre.text)
            for puesto in emp.iter("puesto"):
                auxpuesto.append(puesto.text)
            for salario in emp.iter("salario"):
                auxsalario.append(salario.text)    
        salarios.append(auxsalario)            
        puestos.append(auxpuesto)
        nombres.append(auxnombre)                
        empleado.append(auxid) 
app=Flask(__name__)

@app.route('/')  
def inicio():
    return 'Pantalla de inicio'

@app.route('/ruta1')
def ruta1():
    #body = request.get_json()

    #archivo = body["archivo"]
    #tree = ET.fromstring(archivo)

    arbol=ET.parse('empleados.xml')
    #Obtenemos la raiz getroot con minuscu

    root = arbol.getroot()
    cadena = EmpleadoJson(root)
    objJson = json.loads(cadena)
    Entrada()
    return objJson
    
def Grafos():
    global departamento, empleado, nombres, puestos, salarios
    graf = 'digraph G {\n'
    graf += 'size="10"\n'
    for i in range(len(departamento)):
        graf += f'Empresa->{departamento[i]} \n'
        for j in range(len(empleado[i])):
            graf += f'{departamento[i]}' + '->'  f'"Empleado: {empleado[i][j]}"\n'  
            graf += f'"Empleado: {empleado[i][j]}"'+ '->'  f'"{nombres[i][j]}" \n' 
            graf += f'"Empleado: {empleado[i][j]}"'+ '->'  f'"{puestos[i][j]}" \n' 
            graf += f'"Empleado: {empleado[i][j]}"'+ '->'  f'"{salarios[i][j]} "\n' 
    graf += '}'
    print(graf) 
    grafi = open("Grafo.txt", "w",encoding="utf8")  
    grafi.write(graf)
    grafi.close()
    os.system("dot -Tjpg Grafo.txt -o Grafico.jpg")       
    print("GRAFO CARGADO EXITSAMENTE")



def EmpleadoJson(raiz):
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"
    cantdep = len(raiz.findall('./departamento'))
    cont1 =0
    for departamento in raiz:
        cont1 += 1
        cadena += "{"+"\n"
        nombre=departamento.attrib['departamento']
        cadena+="\"departamento\":"+"\""+nombre+"\","+"\n"
        cadena+="\"empleado\":["+"\n"
        
        cantEmp=len(departamento.findall('./empleado'))
        cont2 =0
        
        for empleado in departamento:
            cont2 += 1
            cadena+="{"+"\n"
            idEmpleado=empleado.attrib['id']
            nombreEmp=empleado.findall('nombre')[0].text
            puestoEmp=empleado.findall('puesto')[0].text
            salarioEmp=empleado.findall('salario')[0].text
            cadena+="\"id\":"+"\""+idEmpleado+"\""+",\n"
            cadena+="\"nombre\":"+"\""+nombreEmp+"\""+",\n"   
            cadena+="\"puesto\":"+"\""+puestoEmp+"\""+",\n"
            cadena+="\"salario\":"+"\""+salarioEmp+"\""+"\n" 
            cadena += "}"+"\n"
            if(cont2<cantEmp):
                cadena+=","+"\n"
        cadena+="]"+"\n"
        cadena+="}"+"\n"
        if(cont1<cantdep):
            cadena+=","+"\n"
    cadena+="]"+"\n"
    cadena+="}"+"\n"
    cadena+="}"
   
    return cadena



@app.route('/modificarEmp',methods = ["POST"])
def ModificarEmpName():
    jasonreq=request.get_json()
    print(jasonreq)
    id_ = jasonreq["id"]
    nombre_ = jasonreq["nombre"]
    tree = ET.parse("empleados.xml")
    ModEmpleadoGeneral(tree, id_, nombre_, "1")
    Entrada()
    return 'listo'



def ModEmpleadoGeneral(tree, id, newname, op):
    
    
    root= tree.getroot()
    var = root.find(f"./departamento/empleado/[@id='{id}']")                     
    if var != None:
        print("Id Valido. ¿Que desea Modificar?")
        print("1. Nombre")
        print("2. Puesto")
        print("3. Sueldo")
        if str(op) == "1" : 
            #name = input("Ingrese nuevo nombre: ")
            for e in var.iter("nombre"):
                print("Anterior: ", e.text)
                e.text = newname
                print("Actual: ", e.text)
                tree.write('empleados.xml',xml_declaration=True,encoding="utf-8")
        elif str(op) == "2":
            #job = input("Ingrese nuevo puesto: ")     
            for e in var.iter("puesto"):
                print("Anterior: ", e.text)
                e.text = job
                print("Actual: ", e.text)
        elif str(op) == "3":
            #salary = input("Ingrese nuevo salario: ")     
            for e in var.iter("salario"):
                print("Anterior: ", e.text)
                e.text = salary
                print("Actual: ", e.text)  
        else: 
            print("condigo no valido")              
    else:
        print("Id no valido, empleado no encontrado")    



@app.route('/reporteempleados')
def reporte():
    Entrada()
    Grafos()
    return 'listo'


@app.route('/empleadoNombre', methods= ["POST"])
def Buscar():
    jsonreq = request.get_json()
    print(jsonreq)
    nombre_ = jsonreq["nombre"]
    cadena = VerEmpleadoN(nombre_)
    obj_jason = json.loads(cadena)
    if cadena != "0":
        return obj_jason
    else: 
        return "No encontrado"
def VerEmpleadoN(busca):
    global departamento,empleado, nombres, puestos, salarios
    print(busca)
    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"
    cantEmp = len(empleado)
    cont2 = 0
    print("cantEMP es: ", cantEmp)
    for i in range (len(empleado)):
        for j in range(len(empleado[i])):
        
            if str(busca) == str(nombres[i][j]):
                
                if(cont2>0):
                    cadena+=","+"\n"    
                cont2 +=1
                cadena += "{"+"\n"
                cadena+="\"departamento\":"+"\""+departamento[i]+"\","+"\n"
                cadena+="\"empleado\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"id\""+":"+ "\""+empleado[i][j]+"\","+"\n"
                cadena+="\"nombre\""+":"+ "\""+nombres[i][j]+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+puestos[i][j]+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+salarios[i][j]+"\""+"\n"
                cadena+="}"+"\n"
                cadena+="]"+"\n"
                cadena += "}"+"\n"
                cont += 1
            else:
                if cont >= 1:
                    cont = cont 
                else: 
                    cont = 0
                    
        

    cadena+="]"+"\n"
    cadena += "}"+"\n"
    cadena += "}"+"\n"  
    if cont == 0:
        return '0'
    else:
        return cadena  

@app.route('/empleadoDepartamento', methods=["POST"])
def Buscar2():
    #jsonreq = request.get_json()
    #print(jsonreq)
    
    depa_ = request.json['departamento']
    cadena = VerDepartamento(depa_)
    obj_json = json.loads(cadena)

    return obj_json


def VerDepartamento(busca): 
    global departamento, empleado, nombres, puestos, salarios
    print(departamento)
    print(busca)
    
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"                              
    

    for i in range (len(departamento)):
        
        if str(busca) == str(departamento[i]):
            cadena += "{"+"\n"
            cadena+="\"departamento\":"+"\""+departamento[i]+"\","+"\n"
            cadena+="\"empleado\":["+"\n"
            cantEmp = len(empleado)
            print("cantEMP es: ", cantEmp)
            cont2 = 0
            
            for j in range(len(empleado[i])):
                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"nombre\""+":"+ "\""+nombres[i][j]+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+puestos[i][j]+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+salarios[i][j]+"\""+"\n"
                cadena+="}"+"\n"
                
                if(cont2<cantEmp):
                    cadena+=","+"\n"
                

            cadena+="]"+"\n"

            cadena += "}"+"\n"

    cadena+="]"+"\n"
    cadena += "}"+"\n"
    cadena += "}"+"\n"

    return cadena
        
@app.route('/empleadoSueldo', methods=["POST"])       
def Buscar3():
    jsonreq = request.get_json()
    print(jsonreq)
    salario_ = jsonreq["salario"]
    cadena = VerEmpleadoS(salario_)
    obj_jason = json.loads(cadena)
    if cadena != "0":
        return obj_jason
    else: 
        return "No encontrado"
def VerEmpleadoS(busca):
    global departamento,empleado, nombres, puestos, salarios
    print(busca)
    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"
    cantEmp = len(empleado)
    cont2 = 0
    print("cantEMP es: ", cantEmp)
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"                              
    

    for i in range (len(departamento)):
        
        if str(busca) == str(departamento[i]):
            cadena += "{"+"\n"
            cadena+="\"departamento\":"+"\""+departamento[i]+"\","+"\n"
            cadena+="\"empleado\":["+"\n"
            cantEmp = len(empleado)
            print("cantEMP es: ", cantEmp)
            cont2 = 0
            
            for j in range(len(empleado[i])):
                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"nombre\""+":"+ "\""+nombres[i][j]+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+puestos[i][j]+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+salarios[i][j]+"\""+"\n"
                cadena+="}"+"\n"
                
                if(cont2<cantEmp):
                    cadena+=","+"\n"
                

            cadena+="]"+"\n"

            cadena += "}"+"\n"

    cadena+="]"+"\n"
    cadena += "}"+"\n"
    cadena += "}"+"\n"

    return cadena

@app.route('/eliminarempleados', methods=["POST"])
def Eliminar():
    jasonreq=request.get_json()
    print(jasonreq)
    id_ = jasonreq["id"]
    tree = ET.parse("empleados.xml")
    EliminarEmpleado(id_, tree)
    return "listo"


def EliminarEmpleado(buscar, tree):
    root = tree.getroot()
    cont = 0
    for dep in root.iter("departamento"):
        for emp in dep.iter("empleado"):
            if buscar == emp.attrib["id"]:
                cont = 1
                dep.remove(emp)
                tree.write('empleados.xml',xml_declaration=True,encoding="utf-8")
            else:
                if cont == 1:
                    cont = 1 
                else: 
                    cont = 0
    if cont == 0:
        print("No encontrado")      



if (__name__== '__main__'):
    
    app.run(debug=True, port = 9000)

