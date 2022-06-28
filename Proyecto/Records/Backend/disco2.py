from textwrap import indent
from xml.dom.minidom import Identified
from flask import Flask,request,render_template
import xml.etree.ElementTree as ET
import json
import re
import os

from flask_cors import CORS

#App va a ser nuestra varianble para crear las rutas POST GET
app=Flask(__name__)
CORS(app)

@app.route('/')
def inicio():
    return 'Pantalla de inicio IPC2'

############################################ eliminar disco
@app.route('/eliminarEmpleado',methods=["POST"])
def discoE():
    jsonres=request.get_json()
    print(jsonres)
    #Guardar en variables los campos del JSON
    titulo=jsonres["title"]
    treeD = ET.parse('disco.xml')
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

    return 'Eliminado Exitosamente'

def eliminarDisco(titulo, treeD, rootD):
    for elem in rootD.findall('cd'):
    # using root.findall() to avoid removal during traversal
        title = str(elem.find('title').text)
        if title == titulo:
            rootD.remove(elem)

    treeD.write("disco2.xml")
    


############################################ modificar disco
@app.route('/modificarEmpleado',methods=["POST"])
def modificarD():

    jsonres=request.get_json()
    print(jsonres)
    #Guardar en variables los campos del JSON
    t=jsonres["title"]
    treeD = ET.parse('disco.xml')
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
    return 'Modificado exitosamente'
                

def mod(title, artist, country, company, price,year, treeD, rootD):
    cambio=False
    for elem in rootD.iter():
        if (str(elem.tag) == "title"):
            if (str(elem.text)==title):
                cambio=True
            else:
                cambio=False

        if (str(elem.tag) == "artist" and cambio==True):
            elem.text=artist
        
        if (str(elem.tag) == "country" and cambio==True):
            elem.text=country

        if (str(elem.tag) == "company" and cambio==True):
            elem.text=company

        if (str(elem.tag) == "price" and cambio==True):
            elem.text=price

        if (str(elem.tag) == "year" and cambio==True):
            elem.text=year
            

    treeD.write("disco2.xml")

    ############################################ agregar disco
@app.route('/agregarDisco',methods=["POST"])
def agregarD():

    jsonres=request.get_json()
    print(jsonres)
    #Guardar en variables los campos del JSON
    #t=jsonres["title"]
    treeD = ET.parse('disco.xml')
    rootD = treeD.getroot()
    
  
    t=jsonres["title"]
    a=jsonres["artist"]
    c=jsonres["country"]
    co=jsonres["company"]
    p=jsonres["price"]
    an=jsonres["year"]
    agregar(t,a,c,co,p,an,treeD, rootD)
    
    return 'Modificado exitosamente'
                

def agregar(title, artist, country, company, price,year, treeD, rootD):

    archivo = open('disco.xml', 'r')           
    carga=archivo.read()
    #print(carga)
    cadena=carga.split()
    #print(cadena)
    tx=""

    for x in cadena:

        if x == '<cd>' or x == '</cd>':
            tx+='\n'

        if x == "</catalog>":
            tx+='<cd> \n'
            tx+='<title>'+title+'</title> \n'
            tx+='<artist>'+artist+'</artist> \n'
            tx+='<country>'+country+'</country> \n'
            tx+='<company>'+company+'</company> \n'
            tx+='<price>'+price+'</price> \n'
            tx+='<year>'+year+'</year> \n'
            tx+='</cd> \n'
        
        tx+=str(x)
        #print(x)
    
    
    file=open('disco3.xml',"w")
    file.write(tx)
    file.close()



    #root = ET.fromstring("<fruits><fruit>banana</fruit><fruit>apple</fruit></fruits>""")
    #tree = ET.ElementTree(root)

    #indent(root)
    # writing xml
    #tree.write("example.xml", encoding="utf-8", xml_declaration=True)


        
    

   
            

    #treeD.write("disco2.xml")


#METODO PRINCIPAL
if(__name__=='__main__'):
    app.run(host="0.0.0.0",port=9000,debug=False)