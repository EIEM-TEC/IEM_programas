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

datos = pd.read_csv("mallas_IEM_comp.csv")

datos.Semestre = datos.Semestre.astype(int)
datos.Columna = datos.Columna.astype(int)
datos.HorasTeoria = datos.HorasTeoria.astype(int)
datos.HorasPractica = datos.HorasPractica.astype(int)
datos.Creditos = datos.Creditos.astype(int)

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
    dump = NoEscape(f"\draw ({round((5*9)/2,1)},{round(4)})")
    dump += NoEscape(f"pic{{titulo={{{titulo},{color}}}}};")
    return dump

def colocar_curso(codigo,nombre,columna,semestre,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(f"\draw ({round(5*columna)},{round(-4*semestre)})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,color):
    dump = NoEscape(f"\draw ({round(0)},{round(-4*semestre)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color}}}}};")
    return dump

def generar_malla(programa):
    cursos = datos[datos.Programa == programa]
    #Geometry
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "0mm",
        "bottom": "0mm",
        "headheight": "1mm",
        "footskip": "1mm"
    }
    #Document options
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper","landscape"],
                   geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    doc.packages.append(Package(name="graphicx"))
    doc.packages.append(Package(name="tikz"))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="xcolor"))
    doc.packages.append(Package(name="colortbl"))
    doc.packages.append(Package(name="array"))
    doc.packages.append(Package(name="float"))
    #doc.packages.append(Package(name="lastpage")) con pagenumbers+true
    doc.packages.append(Package(name="longtable"))
    doc.packages.append(Package(name="multirow"))
    doc.packages.append(Package(name="fancyhdr"))
    
    #bloques

    bloqueTitulo = NoEscape(
    r'''\tikzset{
            pics/titulo/.style args={#1,#2}{
            code={
                \def\ancho{45}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2-2,2*\alto) rectangle (\ancho/2+2,-2*\alto) node[midway,align=center,text width=45cm]{\fontsize{40pt}{0pt}\selectfont \textbf{#1}};
            }
        }
    }'''
    )

    bloqueCurso = NoEscape(
    r'''\tikzset{
            pics/curso/.style args={#1,#2,#3,#4,#5,#6}{
            code={
                \def\ancho{4}
                \def\alto{0.7}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=4cm]{\fontsize{10pt}{12pt}\selectfont {#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#6] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#6] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    )

    bloqueSemestre = NoEscape(
    r'''\tikzset{
            pics/semestre/.style args={#1,#2}{
            code={
                \def\ancho{4}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2,2*\alto) rectangle (\ancho/2,-2*\alto) node[midway,align=center,text width=4cm]{\fontsize{10pt}{12pt}\selectfont \textbf{#1}};
            }
        }
    }'''
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
        malla.append(colocar_titulo(f"Licenciatura en Ingeniería {programa}","lightgray"))
        for semestre in range(0,11):
            malla.append(colocar_semestre(semestre,"lightgray"))
        for codigo in cursos.Codigo:
            nombre = cursos[cursos.Codigo == codigo].Nombre.item()
            columna = cursos[cursos.Codigo == codigo].Columna.item()
            semestre = cursos[cursos.Codigo == codigo].Semestre.item()
            horasteoria = cursos[cursos.Codigo == codigo].HorasTeoria.item()
            horaspractica = cursos[cursos.Codigo == codigo].HorasPractica.item()
            creditos = cursos[cursos.Codigo == codigo].Creditos.item()
            area = cursos[cursos.Codigo == codigo].Area.item()
            comp = cursos[cursos.Codigo == codigo].Compartido.item()
            match comp:
                case "SI":
                    color = "gray"
                case "NO":   
                    color = "white" 
            # match area:
            #     case "Mecánica":
            #         color = "teal"
            #     case "Eléctrica":
            #         color = "gray"
            #     case "Sistemas":
            #         color = "purple"
            #     case "Básicas":
            #         color = "lime"
            #     case "Gestion":
            #         color = "purple"
            #     case "Solido":
            #         color = "teal"
            #     case "Fluidos":
            #         color = "teal"
            #     case "-":
            #         color = "white"
            if semestre <= 10:
                malla.append(colocar_curso(codigo,nombre,columna,semestre,horasteoria,horaspractica,creditos,color))
         
    doc.generate_pdf(f"./mallas/{programa}", clean=True, clean_tex=False, compiler='lualatex')



generar_malla("Electromecánica")
generar_malla("AeronáuticaV2")
generar_malla("AeronáuticaV1")
generar_malla("Mantenimiento Industrial")