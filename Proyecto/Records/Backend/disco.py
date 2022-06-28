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

@app.route('/reporteDiscos')
def discoR():
   
    treeD = ET.parse('disco.xml')
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
    return 'Imagen creada'

#################################################
#busca los discos por su titulo*********************
@app.route('/discoTitulo',methods=["POST"]) 
def discoBT():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    titulo=jsonres["title"]
   
    treeD = ET.parse('disco.xml')
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

####################################################
#busca los discos por su anio*********************
@app.route('/discoYear',methods=["POST"]) 
def discoBA():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    anio=jsonres["year"]
   
    treeD = ET.parse('disco.xml')
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


####################################################
#busca los discos por su artista*********************
@app.route('/discoArtista',methods=["POST"]) 
def discoBArt():
    #leer los datos del json
    jsonres=request.get_json()
    print(jsonres)

    #Guardar en variables los campos del JSON
    art=jsonres["artist"]
   
    treeD = ET.parse('disco.xml')
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









#METODO PRINCIPAL
if(__name__=='__main__'):
    app.run(host="0.0.0.0",port=9000,debug=False)