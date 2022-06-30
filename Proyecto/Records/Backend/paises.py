from flask import Flask,request,render_template
import xml.etree.ElementTree as ET
import json
import re
import os

app = Flask(__name__)
@app.route('/')  
def inicio():
    return 'Pantalla de inicio'

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
    os.system("dot -Tsvg GrafoD.txt -o GraficoP.svg")  
    print("GRAFO CARGADO EXITSAMENTE")            
  


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

@app.route('/reporteRegiones')
def Reporte():
    Entrada()
    Grafico()
    return 'listo'

@app.route('/paisMoneda', methods=["POST"])
def Buscar():
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
def Buscar2():
    jsonreq = request.get_json()
    print(jsonreq)
    idioma_ = jsonreq["idioma"]
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
def Buscar3():
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
if (__name__== '__main__'):
    app.run(host="0.0.0.0", port=8000, debug=False)