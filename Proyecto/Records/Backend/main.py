from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import json
import os
import shutil

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
    #Entrada()
    return objJson


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



@app.route('/modificarEmpleado',methods = ["POST"])
def ModificarEmpName():
    jasonreq=request.get_json()
    print(jasonreq)
    id_ = jasonreq["id"]
    nombre_ = jasonreq["nombre"]
    puesto_ = jasonreq["puesto"]
    salario_ = jasonreq["salario"]

    tree = ET.parse("empleados.xml")
    ModEmpleadoGeneral(tree, id_, nombre_, puesto_, salario_)
    #Entrada()
    return jsonify({"mensaje": "Empleado modificado exitosamente"})



def ModEmpleadoGeneral(tree, id, newname, puesto, salario):
    
    
    root= tree.getroot()
    var = root.find(f"./departamento/empleado/[@id='{id}']")                     
    if var != None:
        #name = input("Ingrese nuevo nombre: ")
        for e in var.iter("nombre"):
            print("Anterior: ", e.text)
            e.text = newname
            print("Actual: ", e.text)
            tree.write('empleados.xml',xml_declaration=True,encoding="utf-8")
        
        #job = input("Ingrese nuevo puesto: ")     
        for e in var.iter("puesto"):
            print("Anterior: ", e.text)
            e.text = puesto
            print("Actual: ", e.text)
            tree.write('empleados.xml',xml_declaration=True,encoding="utf-8")
        
        #salary = input("Ingrese nuevo salario: ")     
        for e in var.iter("salario"):
            print("Anterior: ", e.text)
            e.text = salario
            print("Actual: ", e.text) 
            tree.write('empleados.xml',xml_declaration=True,encoding="utf-8") 
    else: 
            print("condigo no valido")              

@app.route('/reporteEmpleados')
def reporte():
    #Entrada()
    Grafos()
    return jsonify({"Mensaje": "Reporte exitoso"})

def Grafos():
    global departamento, empleado, nombres, puestos, salarios

    doc = ET.parse('empleados.xml')
    root = doc.getroot()

    graf = 'digraph G {\n'
    graf += 'size="10"\n'
    for departamento in root.findall('./departamento'):
        depto = departamento.get('departamento')
        graf += f'Empresa->{depto} \n'
        for empleado in departamento.findall('./empleado'):
            id = empleado.get('id')
            nombre = empleado.find('./nombre').text
            puesto = empleado.find('./puesto').text
            salario = empleado.find('./salario').text
            
            graf += f'{depto}' + '->'  f'"Empleado: {id}"\n'  
            graf += f'"Empleado: {id}"'+ '->'  f'"{nombre}" \n' 
            graf += f'"Empleado: {id}"'+ '->'  f'"{puesto}" \n' 
            graf += f'"Empleado: {id}"'+ '->'  f'"{salario} "\n' 
    graf += '}'
    print(graf) 
    grafi = open("Grafo.txt", "w",encoding="utf8")  
    grafi.write(graf)
    grafi.close()
    os.system("dot -Tjpg Grafo.txt -o Empleados.jpg")       
    print("GRAFO CARGADO EXITSAMENTE")

    
 
    source = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Backend\Empleados.jpg'
    destination = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Frontend\app\static\Empleados.jpg'
    
    shutil.move(source,destination)


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

def VerEmpleadoN(nombre):
    global departamento,empleado, nombres, puestos, salarios
    
    doc = ET.parse('empleados.xml')
    root = doc.getroot()
    cantEmp = 0

    for departamento in root.findall('./departamento'):
        
            for empleado in departamento.findall('./empleado'):

                if str(nombre) == empleado.find('./nombre').text:
                    cantEmp += 1

    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"
    
    

    for departamento in root.findall('./departamento'):
        
        for empleado in departamento.findall('./empleado'):
        
            if str(nombre) == empleado.find('./nombre').text:
                
                cadena += "{"+"\n"
                cadena+="\"departamento\":"+"\""+departamento.get('departamento')+"\","+"\n"
                cadena+="\"empleado\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"id\""+":"+ "\""+empleado.get('id')+"\","+"\n"
                cadena+="\"nombre\""+":"+ "\""+empleado.find('./nombre').text+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+empleado.find('./puesto').text+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+empleado.find('./salario').text+"\""+"\n"
                cadena+="}"+"\n"
                
                if(cantEmp>1):
                    cadena+=","+"\n"  
                
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

    doc = ET.parse('empleados.xml')
    root = doc.getroot()

    print(departamento)
    print(busca)
    
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"                              
    
    print("la lista departamento contiene: ",departamento)
    cantEmp =0 

    for departamento in root.findall('./departamento'):
        
        if str(busca) == departamento.get('departamento'):
            
            for empleado in departamento.findall('./empleado'):
                cantEmp += 1

    for departamento in root.findall('./departamento'):
        
        if str(busca) == departamento.get('departamento'):
            
            cadena += "{"+"\n"
            cadena+="\"departamento\":"+"\""+departamento.get('departamento')+"\","+"\n"
            cadena+="\"empleado\":["+"\n"
            
            cont2 = 0
            
            for empleado in departamento.findall('./empleado'):

                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"nombre\""+":"+ "\""+empleado.find('./nombre').text+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+empleado.find('./puesto').text+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+empleado.find('./salario').text+"\""+"\n"
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
def VerEmpleadoS(sueldo):
    
    doc = ET.parse('empleados.xml')
    root = doc.getroot()
    cantEmp = 0

    for departamento in root.findall('./departamento'):
        
            for empleado in departamento.findall('./empleado'):

                if str(sueldo) == empleado.find('./salario').text:
                    cantEmp += 1

    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"empresa\":{"+"\n"
    cadena+="\"departamento\":["+"\n"
    
    

    for departamento in root.findall('./departamento'):
        
        for empleado in departamento.findall('./empleado'):
        
            if str(sueldo) == empleado.find('./salario').text:
                
                cadena += "{"+"\n"
                cadena+="\"departamento\":"+"\""+departamento.get('departamento')+"\","+"\n"
                cadena+="\"empleado\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"id\""+":"+ "\""+empleado.get('id')+"\","+"\n"
                cadena+="\"nombre\""+":"+ "\""+empleado.find('./nombre').text+"\","+"\n"
                cadena+="\"puesto\""+":"+ "\""+empleado.find('./puesto').text+"\","+"\n"
                cadena+="\"salario\""+":"+ "\""+empleado.find('./salario').text+"\""+"\n"
                cadena+="}"+"\n"
                
                if(cantEmp>1):
                    cadena+=","+"\n"  
                
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



@app.route('/eliminarEmpleado', methods=["POST"])
def Eliminar():
    jasonreq=request.get_json()
    print(jasonreq)
    id_ = jasonreq["id"]
    tree = ET.parse("empleados.xml")
    EliminarEmpleado(id_, tree)
    
    return jsonify({'mensaje':'Eliminado Exitosamente'}) #tiene que retornar un json aunque sea un mensaje sino dara error en el frontend


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


#--------------------------DISCOS---------------------------------
#--------------------------DISCOS---------------------------------
#--------------------------DISCOS---------------------------------


@app.route('/discos')
def disco():
   
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()

    cadenaJson=verDisco(rootD)
   
    objJson=json.loads(cadenaJson)
    return objJson



def verDisco(rootD):
    j=0
    i=0

    tx='''
    {\n
    \"catalog\":{\n
    \"cd\":[\n
    '''
    for elem in rootD.iter():
        
        if (str(elem.tag) == "title"):
            tl=elem.text
            title=tl.replace('"','')
            j=0
            if(i>0):
                
                tx+="},"+"\n"
            
            if(j>0):
                tx+="},"+"\n"

            tx+="{"+"\n"
            

        if (str(elem.tag) == "artist"):
            artist=elem.text
        
        if (str(elem.tag) == "country"):
            country=elem.text

        if (str(elem.tag) == "company"):
            company=elem.text
        
        if (str(elem.tag) == "price"):
            price=elem.text


        if (str(elem.tag) == "year"):
            year=elem.text
            tx+="\"title\":"+"\""+title+"\""+",\n"
            tx+="\"artist\":"+"\""+artist+"\""+",\n"
            tx+="\"country\":"+"\""+country+"\""+",\n"
            tx+="\"company\":"+"\""+company+"\""+",\n"
            tx+="\"price\":"+"\""+price+"\""+",\n"
            tx+="\"year\":"+"\""+year+"\""+"\n"
            i=i+1
            j=j+1

    tx+="}"+"\n"
    tx+="]"+"\n"
    tx+="}"+"\n"
    tx+="}"

    return tx

#---------------------BUSQUEDA DE DISCO POR TITULO-------------------

@app.route('/discoTitulo',methods=["POST"]) 
def discoBT():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    titulo=jsonres["title"]
   
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()

    cadena=buscarDiscoTitulo(rootD,titulo)
   
    objJson=json.loads(cadena)
    return objJson

def buscarDiscoTitulo(rootD,titulo):
    j=0
    i=0
    cambio=False
    tx='''
    {\n
    \"catalog\":{\n
    \"cd\":[\n
    '''
    for elem in rootD.iter():

        if (str(elem.tag) == "title"):
                if (str(elem.text)==titulo):
                    tl=elem.text
                    title=tl.replace('"','')
                    j=0
                    if(i>0):
                        
                        tx+="},"+"\n"
                    
                    if(j>0):
                        tx+="},"+"\n"

                    tx+="{"+"\n"
                    cambio=True
                else:
                    cambio=False

        if (str(elem.tag) == "artist" and cambio==True):
            artist=elem.text
        
        if (str(elem.tag) == "country" and cambio==True):
            country=elem.text

        if (str(elem.tag) == "company" and cambio==True):
            company=elem.text
        
        if (str(elem.tag) == "price" and cambio==True):
            price=elem.text


        if (str(elem.tag) == "year" and cambio==True):
            year=elem.text
            tx+="\"title\":"+"\""+title+"\""+",\n"
            tx+="\"artist\":"+"\""+artist+"\""+",\n"
            tx+="\"country\":"+"\""+country+"\""+",\n"
            tx+="\"company\":"+"\""+company+"\""+",\n"
            tx+="\"price\":"+"\""+price+"\""+",\n"
            tx+="\"year\":"+"\""+year+"\""+"\n"
            i=i+1
            j=j+1

    tx+="}"+"\n"
    tx+="]"+"\n"
    tx+="}"+"\n"
    tx+="}"

    return tx


@app.route('/discoYear',methods=["POST"]) 
def discoBA():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    anio=jsonres["year"]
   
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()

    cadena=buscarDiscoAnio(rootD,anio)
   
    objJson=json.loads(cadena)
    return objJson

def buscarDiscoAnio(rootD,anio):
    j=0
    i=0
    cambio=False
    tx='''
    {\n
    \"catalog\":{\n
    \"cd\":[\n
    '''
    for elem in rootD.iter():

        if (str(elem.tag) == "title"):
            if (cambio==False):
                tl=elem.text
                title=tl.replace('"','')
                j=0
                if(i>0):
                    
                    tx+="},"+"\n"
                
                if(j>0):
                    tx+="},"+"\n"

                tx+="{"+"\n"

        if (str(elem.tag) == "artist"):
            artist=elem.text
        
        if (str(elem.tag) == "country"):
            country=elem.text

        if (str(elem.tag) == "company"):
            company=elem.text
        
        if (str(elem.tag) == "price"):
            price=elem.text


        if (str(elem.tag) == "year"):
            if (str(elem.text)==anio):
                year=elem.text
                tx+="\"title\":"+"\""+title+"\""+",\n"
                tx+="\"artist\":"+"\""+artist+"\""+",\n"
                tx+="\"country\":"+"\""+country+"\""+",\n"
                tx+="\"company\":"+"\""+company+"\""+",\n"
                tx+="\"price\":"+"\""+price+"\""+",\n"
                tx+="\"year\":"+"\""+year+"\""+"\n"
                i=i+1
                j=j+1
                cambio=False
            else:
                cambio=True

           

    tx+="}"+"\n"
    tx+="]"+"\n"
    tx+="}"+"\n"
    tx+="}"

    return tx



@app.route('/discoArtista',methods=["POST"]) 
def discoBArt():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    art=jsonres["artist"]
   
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()

    cadena=buscarDiscoArtista(rootD,art)
   
    objJson=json.loads(cadena)
    return objJson

def buscarDiscoArtista(rootD,art):
    j=0
    i=0
    cambio=False
    txt=""
    tx='''
    {\n
    \"catalog\":{\n
    \"cd\":[\n
    '''
    for elem in rootD.iter():

        if (str(elem.tag) == "title"):
            tl=elem.text
            title=tl.replace('"','')
            

        if (str(elem.tag) == "artist"):
            if (str(elem.text)==art):
                j=0
                if(i>0):
                    
                    tx+="},"+"\n"
                
                if(j>0):
                    tx+="},"+"\n"

                tx+="{"+"\n"
                
                artist=elem.text
                cambio=True
            else:
                cambio=False
        
        if (str(elem.tag) == "country"and cambio==True):
            country=elem.text

        if (str(elem.tag) == "company"and cambio==True):
            company=elem.text
        
        if (str(elem.tag) == "price"and cambio==True):
            price=elem.text


        if (str(elem.tag) == "year"and cambio==True):
            year=elem.text
            tx+="\"title\":"+"\""+title+"\""+",\n"
            tx+="\"artist\":"+"\""+artist+"\""+",\n"
            tx+="\"country\":"+"\""+country+"\""+",\n"
            tx+="\"company\":"+"\""+company+"\""+",\n"
            tx+="\"price\":"+"\""+price+"\""+",\n"
            tx+="\"year\":"+"\""+year+"\""+"\n"
            i=i+1
            j=j+1
          
    tx+="}"+"\n"
    tx+="]"+"\n"
    tx+="}"+"\n"
    tx+="}"

    return tx

@app.route('/eliminarDisco',methods=["POST"])
def discoE():
    jsonres=request.get_json()
    print(jsonres)
    #Guardar en variables los campos del JSON
    titulo=jsonres["title"]
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()
    cambio=False

    for elem in rootD.iter():
        
        if (str(elem.tag) == "title"):
            if (str(elem.text)==titulo):
                eliminarDisco(titulo, treeD, rootD)
                break
            else:
                cambio=False

    if(cambio==False):
        print("Id no encontrado")

    return jsonify({'mensaje':'Eliminado Exitosamente'})

def eliminarDisco(titulo, treeD, rootD):
    for elem in rootD.findall('cd'):
    # using root.findall() to avoid removal during traversal
        title = str(elem.find('title').text)
        if title == titulo:
            rootD.remove(elem)

    treeD.write("discos.xml")


@app.route('/modificarDisco',methods=["POST"])
def modificarD():

    jsonres=request.get_json()
    print(jsonres)
    #Guardar en variables los campos del JSON
    t=jsonres["title"]
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()


    for elem in rootD.iter():
        
        if (str(elem.tag) == "title"):
            if (str(elem.text)==t):
  
                #t=jsonres["title"]
                a=jsonres["artist"]
                c=jsonres["country"]
                co=jsonres["company"]
                p=jsonres["price"]
                an=jsonres["year"]
                mod(t,a,c,co,p,an,treeD, rootD)
    
    return jsonify({"mensaje":"Modificado exitosamente"})
                

def mod(title, artist, country, company, price,year, treeD, rootD):
    cambio=False
    for elem in rootD.iter():
        if (str(elem.tag) == "title"):
            if (str(elem.text)==title):
                cambio=True
                if (str(elem.tag) == "artist" and cambio==True):
                    elem.text=artist
                    treeD.write("discos.xml")
            
                if (str(elem.tag) == "country" and cambio==True):
                    elem.text=country
                    treeD.write("discos.xml")

                if (str(elem.tag) == "company" and cambio==True):
                    elem.text=company
                    treeD.write("discos.xml")

                if (str(elem.tag) == "price" and cambio==True):
                    elem.text=price
                    treeD.write("discos.xml")

                if (str(elem.tag) == "year" and cambio==True):
                    elem.text=year
                    treeD.write("discos.xml")
            else:
                cambio=False

            
            

        #treeD.write("discos.xml")



@app.route('/reporteDiscos')
def discoR():
   
    treeD = ET.parse('discos.xml')
    rootD = treeD.getroot()

    respuesta=graficoD(rootD)
   
    #objJson=json.loads(cadenaJson)
    return respuesta

def graficoD(rootD):
    n=0
    m=0
    o=0
    tx='''
        digraph G {
            fontname="Helvetica,Arial,sans-serif"
            node [fontname="Helvetica,Arial,sans-serif"]
            edge [fontname="Helvetica,Arial,sans-serif"]
            concentrate=True;
            rankdir=TB;
            node [shape=record];
    
    '''
    tx = tx+ 'n'+str(n)+' [label="Disco"]; \n'
    for elem in rootD.iter():
        
        if (str(elem.tag) == "title"):
            m=m+1
            tx = tx+ 'nD'+str(m)+' [label="cd"]; \n'
            tx=tx+'n0 -> '+'nD'+str(m)+'; \n'
            tl=elem.text
            title=tl.replace('"','')
            o=o+1
            tx = tx+ 'nT'+str(m)+' [label="'+str(title)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nT'+str(o)+'; \n'

        if (str(elem.tag) == "artist"):
            artist=elem.text
            tx = tx+ 'nA'+str(m)+' [label="Artist= '+str(artist)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nA'+str(o)+'; \n'
        
        if (str(elem.tag) == "country"):
            country=elem.text
            tx = tx+ 'nC'+str(m)+' [label="Country= '+str(country)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nC'+str(o)+'; \n'

        if (str(elem.tag) == "company"):
            company=elem.text
            tx = tx+ 'nCO'+str(m)+' [label="Company= '+str(company)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nCO'+str(o)+'; \n'
        
        if (str(elem.tag) == "price"):
            price=elem.text
            tx = tx+ 'nP'+str(m)+' [label="Price= '+str(price)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nP'+str(o)+'; \n'


        if (str(elem.tag) == "year"):
            year=elem.text
            tx = tx+ 'nAN'+str(m)+' [label="Year= '+str(year)+'"]; \n'
            tx=tx+'nD'+str(m)+' -> '+'nAN'+str(o)+'; \n'
            

    tx=tx+'}'
    print("Se a generado Imagen")
    file = open("disco.dot", "w")
    file.write(tx)
    file.close()
        
        #import os
    os.system("dot disco.dot -Tpng -o disco.png")

    source = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Backend\disco.png'
    destination = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Frontend\app\static\disco.png'
    
    shutil.move(source,destination)

    return jsonify({"mensaje":"Imagen Creada"})




continentes = []
pasises = []
def Entrada():
    continentes.clear()
    pasises.clear()
    tree = ET.parse('paises.xml')
    root = tree.getroot()
    for continente in root.iter("continente"):
        auxpais = []
        continentes.append(continente.attrib["name"])
        for pais in continente.iter("pais"):
            aux2pais = []
            aux2pais.append(pais.attrib["moneda"])
            for nombre in pais.iter("nombre"):
                aux2pais.append(nombre.text)
            for capital in pais.iter("capital"):
                aux2pais.append(capital.text)
            for idioma in pais.iter("idioma"):
                aux2pais.append(idioma.text)
            auxpais.append(aux2pais)    
        pasises.append(auxpais)        
    print(continentes)  
    print(pasises)              
    
     
  
#---------------------------------------PAISES-------------------------------------
#---------------------------------------PAISES-------------------------------------
#---------------------------------------PAISES-------------------------------------

@app.route('/paises')
def Ver():
    tree = ET.parse('paises.xml')
    root = tree.getroot()
    cadena = Verpaises(root)
    obj_jason = json.loads(cadena)
    Entrada()
    return obj_jason
def Verpaises(raiz):
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"mundo\":{"+"\n"
    cadena+="\"continente\":["+"\n"
    cantCont = len(raiz.findall('./continente'))
    cont1 = 0
    for continente in raiz:
        cont1 +=1
        cadena += "{"+"\n"
        nombrec=continente.attrib['name']
        cadena+="\"continente\":"+"\""+nombrec+"\","+"\n"
        cadena+="\"pais\":["+"\n"
        cantpais = len(continente.findall('./pais')) 
        cont2 = 0
        
        for pais in continente:
            cont2 += 1
            cadena+="{"+"\n"
            moneda = pais.attrib['moneda']
            nombre = pais.findall('nombre')[0].text
            capital = pais.findall('capital')[0].text
            idioma = pais.findall('idioma')[0].text
            cadena+="\"moneda\":"+"\""+moneda+"\""+",\n"
            cadena+="\"nombre\":"+"\""+nombre+"\""+",\n"
            cadena+="\"capital\":"+"\""+capital+"\""+",\n"
            cadena+="\"idioma\":"+"\""+idioma+"\""+"\n"
            cadena += "}"+"\n"
            if(cont2<cantpais):
                cadena+=","+"\n"
        cadena+="]"+"\n"
        cadena+="}"+"\n"
        if(cont1<cantCont):
            cadena+=","+"\n"
    cadena+="]"+"\n"
    cadena+="}"+"\n"
    cadena+="}"
    print(cadena)
    return cadena

@app.route('/paisMoneda', methods=["POST"])
def buscarMoneda():
    jsonreq = request.get_json()
    print(jsonreq)
    moneda_ = jsonreq["moneda"]
    cadena = VerMoneda(moneda_)
    obj_jason = json.loads(cadena)
    if cadena != "0":
        return obj_jason
    else: 
        return "No encontrado"

def VerMoneda(buscar):
    global continentes, pasises
    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"mundo\":{"+"\n"
    cadena+="\"continente\":["+"\n"
    cont2 = 0
    for i in range(len(pasises)):
        for j in range(len(pasises[i])):
            if str(buscar) == str(pasises[i][j][0]):
                if(cont2>0):
                    cadena+=","+"\n"    
                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"continente\":"+"\""+continentes[i]+"\","+"\n"
                cadena+="\"pais\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"moneda\":"+"\""+pasises[i][j][0]+"\""+",\n"
                cadena+="\"nombre\":"+"\""+pasises[i][j][1]+"\""+",\n"
                cadena+="\"capital\":"+"\""+pasises[i][j][2]+"\""+",\n"
                cadena+="\"idioma\":"+"\""+pasises[i][j][3]+"\""+"\n"
                cadena += "}"+"\n"
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

@app.route('/paisIdioma', methods=["POST"])
def BuscarIdioma():
    jsonreq = request.get_json()
    print("el idioma es: ",jsonreq)
    idioma_ = jsonreq['idioma']
    cadena = VerIdioma(idioma_)
    obj_jason = json.loads(cadena)
    if cadena != "0":
        return obj_jason
    else: 
        return "No encontrado"
def VerIdioma(buscar):
    global continentes, pasises
    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"mundo\":{"+"\n"
    cadena+="\"continente\":["+"\n"
    cont2 = 0
    for i in range(len(pasises)):
        for j in range(len(pasises[i])):
            if str(buscar) == str(pasises[i][j][3]):
                if(cont2>0):
                    cadena+=","+"\n"    
                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"continente\":"+"\""+continentes[i]+"\","+"\n"
                cadena+="\"pais\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"moneda\":"+"\""+pasises[i][j][0]+"\""+",\n"
                cadena+="\"nombre\":"+"\""+pasises[i][j][1]+"\""+",\n"
                cadena+="\"capital\":"+"\""+pasises[i][j][2]+"\""+",\n"
                cadena+="\"idioma\":"+"\""+pasises[i][j][3]+"\""+"\n"
                cadena += "}"+"\n"
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
    
@app.route('/continente', methods=["POST"])
def buscarContinente():
    jsonreq = request.get_json()
    print(jsonreq)
    continente_ = jsonreq["continente"]
    cadena = VerContinente(continente_)
    obj_jason = json.loads(cadena)
    if cadena != "0":
        return obj_jason
    else: 
        return "No encontrado"
def VerContinente(buscar):
    global continentes, pasises
    cont = 0
    cadena = ""
    cadena+="{"+"\n"
    cadena+="\"mundo\":{"+"\n"
    cadena+="\"continente\":["+"\n"
    cont2 = 0
    for i in range(len(continentes)):
        if str(buscar) == str(continentes[i]):
            for j in range(len(pasises[i])):
                if(cont2>0):
                    cadena+=","+"\n"    
                cont2 +=1
                cadena+="{"+"\n"
                cadena+="\"continente\":"+"\""+continentes[i]+"\","+"\n"
                cadena+="\"pais\":["+"\n"
                cadena+="{"+"\n"
                cadena+="\"moneda\":"+"\""+pasises[i][j][0]+"\""+",\n"
                cadena+="\"nombre\":"+"\""+pasises[i][j][1]+"\""+",\n"
                cadena+="\"capital\":"+"\""+pasises[i][j][2]+"\""+",\n"
                cadena+="\"idioma\":"+"\""+pasises[i][j][3]+"\""+"\n"
                cadena += "}"+"\n"
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

@app.route('/reportePaises')
def Reporte():
    Entrada()
    Grafico()
    return jsonify({"mensaje":"Grafico de Paises creado exitosamente"})

def Grafico():
    graf = 'digraph G {\n'
    graf += 'size="10"\n'
    cont = 0
    cont2 = 0
    for i in range(len(pasises)):
        for j in range(len(pasises[i])):
            #for k in range(len(pasises[i][j])):
                graf += f'a{cont}' + '[label=' + f'"{pasises[i][j][0]}"]\n'
                #graf += f'b{cont}' + '[label=' + f'"{pasises[i][j][1]}"]\n'
                graf += f'c{cont}' + '[label=' + f'"{pasises[i][j][2]}"]\n'
                graf += f'd{cont}' + '[label=' + f'"{pasises[i][j][3]}"]\n'
                cont += 1
                
    for i in range(len(continentes)):
        graf += f'Mundo->{continentes[i]} \n'
        
        for j in range (len(pasises[i])):
            graf += f'{continentes[i]}->' + f'"{pasises[i][j][1]}" \n'
            graf += f'"{pasises[i][j][1]}"  ->' +f'a{cont2} \n'
            graf += f'"{pasises[i][j][1]}"  ->' +f'c{cont2} \n'
            graf += f'"{pasises[i][j][1]}"  ->' +f'd{cont2} \n'
            cont2 += 1
    graf += '}'
    print(graf) 
    grafi = open("GrafoD.txt", "w",encoding="utf8")  
    grafi.write(graf)
    grafi.close()
    os.system("dot -Tsvg GrafoD.txt -o Paises.svg")  
    print("GRAFO CARGADO EXITSAMENTE")   

    source = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Backend\Paises.svg'
    destination = r'C:\Users\Darkun\Desktop\IPC2 - 2022\IPC2 VACAS 2022\IPC2_2022\Proyecto\Records\Frontend\app\static\Paises.svg'
    
    shutil.move(source,destination)    


if (__name__== '__main__'):
    
    app.run(debug=True, port = 9000)


