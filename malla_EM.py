import os
import roman
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZScope, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic

datos = pd.read_csv("malla_EM.csv",
    dtype = {'Codigo':str,'Nombre':str,'Area':str,'Semestre':int,'Fila':int,'HorasTeoria':int,'HorasPractica':int,'Creditos':int})

def textcolor(size,vspace,color,bold,text,hspace="0"):
    dump = NoEscape(r"\par")
    if hspace!="0":
        dump += NoEscape(HorizontalSpace(hspace,star=True).dumps())
    dump += NoEscape(Command("fontsize",arguments=Arguments(size,vspace)).dumps())
    dump += NoEscape(Command("selectfont").dumps()) + NoEscape(" ")
    if bold==True:
        dump += NoEscape(Command("textbf", NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())).dumps())
    else:
        dump += NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())
    return dump

def colocar_titulo(titulo,color):
    dump = NoEscape(f"\draw ({round(57/2)},{round(4)})")
    dump += NoEscape(f"pic{{titulo={{{titulo},{color}}}}};")
    return dump

def colocar_curso(codigo,nombre,fila,semestre,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(f"\draw ({round(6.87*semestre,2)+0.5},{round(-4.2*fila,1)-0.5})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,color,horasteoriasemestre,horaspracticasemestre,creditossemestre):
    dump = NoEscape(f"\draw ({round(6.87*semestre,2)+0.5},{round(0)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    return dump



def generar_TC(programa,plan):
    cred_TC = [0,0,0,0,0,0,0,0,0,0,0]
    cred_acum = []
    acumulado = 0
    nombreProg = "Ingeniería Electromecánica - Tronco Común"
    #Geometría
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "1mm",
        "bottom": "0mm",
        "headheight": "1mm",
        "footskip": "1mm"
    }
    #Opciones del documento
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper","landscape"],
                   geometry_options=geometry_options)
    #Paquetes
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    doc.packages.append(Package(name="graphicx"))
    doc.packages.append(Package(name="tikz"))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="xcolor",options="dvipsnames"))
    doc.packages.append(Package(name="colortbl"))
    doc.packages.append(Package(name="array"))
    doc.packages.append(Package(name="float"))
    doc.packages.append(Package(name="longtable"))
    doc.packages.append(Package(name="multirow"))
    doc.packages.append(Package(name="fancyhdr"))
    #Bloques
    bloqueTitulo = NoEscape(
    r'''\tikzset{
            pics/titulo/.style args={#1,#2}{
            code={
                \def\ancho{57}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2-2,2*\alto) rectangle (\ancho/2+2,-2*\alto) node[midway,align=center,text width=45cm]{\fontsize{30pt}{0pt}\selectfont \textbf{#1}};
            }
        }
    }'''
    )
    bloqueCurso = NoEscape(
    r'''\tikzset{
            pics/curso/.style args={#1,#2,#3,#4,#5,#6}{
            code={
                \def\ancho{5}
                \def\alto{0.8}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=\ancho cm]{\fontsize{14pt}{2pt}\selectfont {#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #3};
                \draw[fill=#6] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#6] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }''' 
    #1: codigo, #2: nombre, #3: horasteoria, #4: horaspractica, #5: creditos, #6: color
    )
    bloqueSemestre = NoEscape(
    r'''\tikzset{
            pics/semestre/.style args={#1,#2,#3,#4,#5}{
            code={
                \def\ancho{6}
                \def\alto{0.8}
                \draw[fill=#2] (-\ancho/2,1.5*\alto) rectangle (\ancho/2,-1.5*\alto) node[midway,align=center,text width=6cm]{\fontsize{16pt}{12pt}\selectfont \textbf{#1}};
                \draw[fill=#2] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#2] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#2] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    #1: semestre, #2: color, #3: horasteoria, #4: horaspractica, #5: creditos
    )
    doc.preamble.append(bloqueTitulo)        
    doc.preamble.append(bloqueCurso)
    doc.preamble.append(bloqueSemestre)
    doc.append(Command('centering'))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla:
        # malla.append(NoEscape(r"\draw (,0)--(45,-2);"))
        malla.append(colocar_titulo(f"{nombreProg} - Plan: {plan}","lightgray"))
        for semestre in range(0,9):
            horasteoriasemestre = datos[datos.Semestre == semestre].HorasTeoria.sum()
            horaspracticasemestre = datos[datos.Semestre == semestre].HorasPractica.sum()
            creditossemestre = datos[datos.Semestre == semestre].Creditos.sum()
            malla.append(colocar_semestre(semestre,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for codigo in datos.Codigo:
            nombre = datos[datos.Codigo == codigo].Nombre.item()
            fila = datos[datos.Codigo == codigo].Fila.item()
            semestre = datos[datos.Codigo == codigo].Semestre.item()
            horasteoria = datos[datos.Codigo == codigo].HorasTeoria.item()
            horaspractica = datos[datos.Codigo == codigo].HorasPractica.item()
            creditos = datos[datos.Codigo == codigo].Creditos.item()
            area = datos[datos.Codigo == codigo].Area.item()
            match area:
                case "CIB":
                    color = "Apricot"
                    i = 0
                case "FPH":
                    print(nombre)
                    color = "Aquamarine"
                    i = 1
                case "CYD":
                    color = "Lavender"
                    i = 2
                case "IEE":
                    color = "LimeGreen"
                    i = 3
                case "IMM":
                    color = "WildStrawberry"
                    i = 4
                case "AUT":
                    color = "Tan"
                    i = 5
                case "ADD":
                    color = "YellowOrange"
                    i = 6
                case "INS":
                    color = "white"
                    i = 7
                case "AER":
                    color = "white"
                    i = 8
                case "SCB":
                    color = "white"
                    i = 9
            if area in ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]:                    
                cred_TC[i] = cred_TC[i] + creditos
                acumulado = acumulado + creditos
                malla.append(colocar_curso(codigo,nombre,fila,semestre,horasteoria,horaspractica,creditos,color))
            cred_TC[10] = acumulado
            # if acumulado < 108:
            #     color = "green"
            # elif acumulado < 135:
            #     color = "yellow"
            # else:
            #     color = "white"                
    cred_acum.append(cred_TC)
    cred_TC = [(x/acumulado)*100 for x in cred_TC]
    cred_acum.append(cred_TC)
    acum_cred = pd.DataFrame(cred_acum, columns=["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS","AER","SCB","Total"]) 
    acum_cred.insert(0,'detalle',["Creditos TC", "Porcentajes TC"])
    print(acum_cred)
    doc.generate_pdf(f"./mallas/{programa}-{plan}", clean=True, clean_tex=False, compiler='lualatex',silent=True)

generar_TC('EM','0001')
