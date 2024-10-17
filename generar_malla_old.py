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

datos = pd.read_csv("mallas_IEM.csv",
    dtype = {'Codigo':str,'Programa':str,'Plan':str,'Semestre':int,'Fila':int,'HorasTeoria':int,'HorasPractica':int,'Creditos':int})
nombresCurs = pd.read_csv("cursos_IEM.csv")
nombresProg = pd.read_csv("nombres_programas.csv")


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
    dump = NoEscape(f"\draw ({round(27)},{round(4)})")
    dump += NoEscape(f"pic{{titulo={{{titulo},{color}}}}};")
    return dump

def colocar_curso(codigo,nombre,fila,semestre,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(f"\draw ({round(-4*semestre)},{round(5*fila)})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,color,horasteoriasemestre,horaspracticasemestre,creditossemestre):
    dump = NoEscape(f"\draw ({round(5*semestre)},{round(0)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    return dump

def generar_malla(programa,plan):
    acumulado = 0
    cursos = datos[datos.Programa == programa]
    cursos = cursos[cursos.Plan == plan]
    nombreProg = nombresProg[nombresProg.Programa == programa].NomPrograma.item()
    #Geometría
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "2mm",
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
    doc.packages.append(Package(name="xcolor"))
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
                \def\ancho{45}
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
                \def\ancho{8}
                \def\alto{1.5}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=4cm]{\fontsize{8.5pt}{2pt}\selectfont {#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
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
                \def\ancho{4}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2,1.5*\alto) rectangle (\ancho/2,-1.5*\alto) node[midway,align=center,text width=4cm]{\fontsize{10pt}{12pt}\selectfont \textbf{#1}};
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
        for semestre in range(0,11):
            horasteoriasemestre = cursos[cursos.Semestre == semestre].HorasTeoria.sum()
            horaspracticasemestre = cursos[cursos.Semestre == semestre].HorasPractica.sum()
            creditossemestre = cursos[cursos.Semestre == semestre].Creditos.sum()
            malla.append(colocar_semestre(semestre,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        # for codigo in cursos.Codigo:
        #     nombre = nombresCurs[nombresCurs.Codigo == codigo].Nombre.item()
        #     fila = cursos[cursos.Codigo == codigo].Fila.item()
        #     semestre = cursos[cursos.Codigo == codigo].Semestre.item()
        #     horasteoria = cursos[cursos.Codigo == codigo].HorasTeoria.item()
        #     horaspractica = cursos[cursos.Codigo == codigo].HorasPractica.item()
        #     creditos = cursos[cursos.Codigo == codigo].Creditos.item()
        #     #area = cursos[cursos.Codigo == codigo].Area.item()
        #     # match area:
        #     #     case "Mecánica":
        #     #         color = "teal"
        #     #     case "Eléctrica":
        #     #         color = "gray"
        #     #     case "Sistemas":
        #     #         color = "purple"
        #     #     case "Básicas":
        #     #         color = "lime"
        #     #     case "Gestion":
        #     #         color = "purple"
        #     #     case "Solido":
        #     #         color = "teal"
        #     #     case "Fluidos":
        #     #         color = "teal"
        #     #     case "-":
        #     #         color = "white"
        #     acumulado = acumulado + creditos
        #     if acumulado < 108:
        #         color = "green"
        #     elif acumulado < 135:
        #         color = "yellow"
        #     else:
        #         color = "white"
        #     if semestre <= 10:
        #         malla.append(colocar_curso(codigo,nombre,fila,semestre,horasteoria,horaspractica,creditos,color))
    doc.generate_pdf(f"./mallas/{programa}-{plan}", clean=True, clean_tex=False, compiler='lualatex',silent=True)


# generar_malla('MI','1313')
# generar_malla('AE','0001')
generar_malla('EM','0001')
# generar_malla('MA','0001')