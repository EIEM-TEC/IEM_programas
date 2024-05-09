import subprocess
import time
import pandas as pd
import numpy as np
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable, LongTabu, LongTabularx, Tabularx, Tabular,\
    config
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic

def textcolor(size,vspace,color,bold,text,hspace="0",par=True):
    dump = NoEscape(r"")
    if par==True:
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

def VarCol(ltext,rtext):
    dump = NoEscape(
r'''
\begin{tcolorbox}[
blanker,
width=0.78\textwidth,enlarge left by=0.24\textwidth,
before skip=6pt,
breakable,
overlay unbroken and first={%
    \node[inner sep=0pt,outer sep=0pt,text width=0.22\textwidth,
    align=none,
    below right]
    at ([xshift=-0.24\textwidth]frame.north west)
{
'''
    )
    dump += textcolor(   
            par=False,
            hspace="0mm",
            size="12",
            vspace="14",
            color="parte",
            bold=True,
            text=f"{ltext}" 
            )
    dump += NoEscape(
r'''
};}]
'''
    )
    dump += NoEscape(rtext)
    dump += NoEscape(
r''' 
\end{tcolorbox}
'''
    )
    return dump

def number_to_ordinals(number_str):
    match number_str:
        case "1" | "3":
            number_str += r"\textsuperscript{er}"
        case "2":
            number_str += r"\textsuperscript{do}"
        case "4" | "5" | "6":
            number_str += r"\textsuperscript{to}"
        case "7" | "10":
            number_str += r"\textsuperscript{mo}"
        case "8":
            number_str += r"\textsuperscript{vo}"
        case "9":
            number_str += r"\textsuperscript{no}"
    return number_str 

cursos = pd.read_csv("cursos_IEM.csv")
datos_gen = pd.read_csv("datos_IEM.csv")
descrip_obj = pd.read_csv("descrip_obj_IEM.csv")
profes = pd.read_csv("profesores.csv")

def generar_programa(codigo,listProf):
    codCurso = codigo
    nomEscue = "Escuela de Ingeniería Electromecánica"
    lisProgr = cursos[cursos.Codigo == codCurso].Programas.str.split('\n',expand=False).explode()
    lisProgr = lisProgr.str.split(';',expand=True)
    lisProgr.reset_index(inplace = True, drop = True)
    lisProgr.columns = ['programa','semestre']
    if len(lisProgr) > 1:
        strProgr = "Carreras de: " + ' e'.join(lisProgr['programa'].str.cat(sep='; ').rsplit(';',1))
    else:
        strProgr = "Carrera de " + lisProgr['programa'].item() + "."
    nomCurso = cursos[cursos.Codigo == codCurso].Nombre.item()
    areCurso = datos_gen[datos_gen.Codigo == codCurso].Area.item()
    areCurso = areCurso[0].lower() + areCurso[1:len(areCurso)]
    tipCurso = datos_gen[datos_gen.Codigo == codCurso].Tipo.item()
    eleCurso = datos_gen[datos_gen.Codigo == codCurso].Electivo.item()
    porAreas = datos_gen[datos_gen.Codigo == codCurso].AreasCurriculares.item()
    #Genera ubicación en el plan de estudios en las diferentes carreras
    ubiPlane = ""
    for sem in np.sort(lisProgr['semestre'].unique()):
        filter = lisProgr["semestre"] == str(sem)
        filterlist = lisProgr[filter]
        ubiPlane += "Curso de "
        ubiPlane += number_to_ordinals(str(sem))
        ubiPlane += " semestre en "
        if len(filterlist)  > 1:
            ubiPlane += ' e'.join(filterlist['programa'].str.cat(sep='; ').rsplit(';',1)) + ". "
        else:
            ubiPlane += filterlist['programa'].item() + ". "
    susRequi = datos_gen[datos_gen.Codigo == codCurso].Requisitos.item()
    corRequi = datos_gen[datos_gen.Codigo == codCurso].Correquisitos.item()
    essRequi = datos_gen[datos_gen.Codigo == codCurso].EsRequisito.item()
    tipAsist = datos_gen[datos_gen.Codigo == codCurso].Asistencia.item()
    posRecon = datos_gen[datos_gen.Codigo == codCurso].PosibilidadReconocimiento.item()
    posSufic = datos_gen[datos_gen.Codigo == codCurso].PosibilidadSuficiencia.item()
    numCredi = datos_gen[datos_gen.Codigo == codCurso].Creditos.item()
    horClass = datos_gen[datos_gen.Codigo == codCurso].HorasClase.item()
    horExtra = datos_gen[datos_gen.Codigo == codCurso].HorasExtraclase.item()
    vigProgr = datos_gen[datos_gen.Codigo == codCurso].Vigencia.item()
    desGener = descrip_obj[descrip_obj.Codigo == codCurso].Descripcion.item()
    objGener = descrip_obj[descrip_obj.Codigo == codCurso].ObjetivoGeneral.item()
    objGener = objGener[0].lower() + objGener[1:len(objGener)] # primera letra en minuscula
    objCurso = f"Al final del curso la persona estudiante será capaz de {objGener}" + r'\\' + '\n'\
    + "La persona estudiante será capaz de:" + r'\\' + '\n'
    objEspec = descrip_obj[descrip_obj.Codigo == codCurso].ObjetivosEspecificos.str.split('\n',expand=False).explode()
    for index, row in objEspec.items():     
        objCurso += r"\hspace*{0.02\linewidth}\parbox{0.98\linewidth}{\strut\textbullet\, " + row + r"\strut}\\" + '\n'
    conCurso = descrip_obj[descrip_obj.Codigo == codCurso].Contenidos.str.split('\r\n',expand=False).explode()
    conCurso.reset_index(inplace = True, drop = True)
    nivel_1, nivel_2, nivel_3 = [0,0,0]
    for index, row in conCurso.items():
        res = 0
        for pos in range(3):
            if pos == row.find('*', pos, pos+1):
                res += 1
        if res == 1:
            nivel_1 += 1
            nivel_2 = 0
            conCurso.iloc[index] = row.replace('*', f"{str(nivel_1)}. ")
        elif res == 2:
            nivel_2 += 1
            nivel_3 = 0
            conCurso.iloc[index] = r"\hspace*{0.02\linewidth}\parbox{0.98\linewidth}{\strut " + row.replace('**', f"{str(nivel_1)}.{str(nivel_2)}. ") + r"\strut}"
        elif res == 3:
            nivel_3 += 1
            conCurso.iloc[index] = r"\hspace*{0.04\linewidth}\parbox{0.96\linewidth}{\strut " + row.replace('***', f"{str(nivel_1)}.{str(nivel_2)}.{str(nivel_3)}. ") + r"\strut}"
    conCursoStr = (r'\\'+'\n').join(conCurso) + r'\\'
    metCurso = descrip_obj[descrip_obj.Codigo == codCurso].Metodologia.item()
    evaCurso = descrip_obj[descrip_obj.Codigo == codCurso].Evaluacion.str.split('\n',expand=False).explode()
    evaCurso = evaCurso.str.split(';',expand=True)
    evaCurso.reset_index(inplace = True, drop = True)
    evaCurso.columns = ['2','3','4']
    evaCurso[['0','1','5']] = ""
    evaCurso.sort_index(axis=1, inplace=True)
    bibCurso = NoEscape('\n'+ r'\nocite{' + ('}\n'+r'\nocite{').join(descrip_obj[descrip_obj.Codigo == codCurso].Bibtex.item().split(';')) + '}\n' + r'\printbibliography[heading=none]')
    filProfe = profes[profes.Codigo.isin(listProf)]
    proCurso = r"" 
    for index, row in filProfe.iterrows():
        titulo = row['Titulo']
        match titulo:
            case "M.Sc." | "Ing." | "Máster":
                proCurso += \
                row['Titulo'] + " "\
                + row['Nombre']
            case "Ph.D.":
                proCurso += \
                row['Nombre'] + " "\
                + row['Titulo']
        proCurso += r'\\' + '\n'
        for i in range(len(row['Titulos'].split('\r\n'))):
            proCurso += row['Titulos'].split('\r\n')[i] + r'\\' + '\n'
        proCurso += \
        'Correo: ' + row['Correo']\
        + '. Oficina: ' + str(row['Oficina']) + r'\\' + '\n'\
        + 'Escuela de ' + row['Escuela']\
        + '. ' + row['Sede'] + r'\\[12pt]' + '\n'                    
    #Config
    config.active = config.Version1(row_heigth=1.5)
    #Geometry
    geometry_options = { 
        "left": "22.5mm",
        "right": "16.1mm",
        "top": "48mm",
        "bottom": "25mm",
        "headheight": "12.5mm",
        "footskip": "12.5mm"
    }
    #Document options
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper"],
                   geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish','activeacute']))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="fancyhdr"))
    doc.packages.append(Package(name="csquotes"))
    doc.packages.append(Package(name="biblatex", options=['style=ieee','backend=biber']))
    doc.packages.append(Package(name="tcolorbox",options=['skins','breakable']))
    #Package options
    doc.preamble.append(Command('setmainfont','Arial'))
    #doc.preamble.append(Command('usetikzlibrary','calc'))
    #doc.preamble.append(Command('linespread', '0.9'))
    doc.preamble.append(Command('addbibresource', '../bibliografia.bib'))
    doc.preamble.append(NoEscape(r'\renewcommand*{\bibfont}{\fontsize{12}{16}\selectfont}'))
    doc.add_color('gris','rgb','0.27,0.27,0.27') #70,70,70
    doc.add_color('parte','rgb','0.02,0.204,0.404') #5,52,103
    doc.add_color('azulsuaveTEC','rgb','0.02,0.455,0.773') #5,116,197
    doc.add_color('fila','rgb','0.929,0.929,0.929') #237,237,237
    doc.add_color('linea','rgb','0.749,0.749,0.749') #191,191,191

    headerfooter = PageStyle("headfoot")

    #Left header
    with headerfooter.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=r"0.5\textwidth",align="l")) as logobox:
            logobox.append(StandAloneGraphic(image_options="width=62.5mm", filename='../figuras/Logo.png'))
    #Left foot
    with headerfooter.create(Foot("L")) as footer_left:
        footer_left.append(TextColor("azulsuaveTEC", f"{nomEscue}"))
        footer_left.append(NoEscape(r"\par \parbox{0.85\textwidth}{"))
        footer_left.append(textcolor
            (   
            par=False,
            size="8",
            vspace="0",
            color="azulsuaveTEC",
            bold=False,
            text=f"{strProgr}" 
            ))
        footer_left.append(NoEscape(r"}"))
    #Right foot
    with headerfooter.create(Foot("R")) as footer_right:
        footer_right.append(TextColor("azulsuaveTEC", NoEscape(r"Página \thepage \hspace{1pt} de \pageref*{LastPage}")))        
  
    title = NoEscape(
    r'''
    \vspace*{170mm}

    \fontsize{14}{0}\selectfont Programa del curso \codCurso

    \fontsize{18}{25}\selectfont \textbf{\textcolor{azulsuaveTEC}{\nomCurso}}

    \hspace*{10mm}\fontsize{12}{40}\selectfont \color{black!40!gray}\nomEscue

    \hspace*{10mm}\fontsize{12}{14}\selectfont \color{black!40!gray}\nomProgr
    '''
    )

    doc.preamble.append(headerfooter)
    doc.change_page_style("empty")
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "overlay",
                "remember picture"
                )
        )) as logo:
        logo.append(TikZNode(\
            options=TikZOptions
                (
                "inner sep = 0mm",
                "outer sep = 0mm",
                "anchor = north west",
                "xshift = -23mm",
                "yshift = 22mm"
                ),
            text=StandAloneGraphic(image_options="width=21cm", filename='../figuras/Logo_portada.png').dumps(),\
            at=TikZCoordinate(0,0)
        ))
    doc.append(VerticalSpace("150mm", star=True))
    doc.append(textcolor
            (   
            size="14",
            vspace="0",
            color="black",
            bold=False,
            text=f"Programa del curso {codCurso}" 
            ))
    doc.append(textcolor
            (  
            size="18",
            vspace="25",
            color="azulsuaveTEC",
            bold=True,
            text=f"{nomCurso}" 
            ))
    with doc.create(Tabularx(table_spec=r"m{0.02\textwidth}m{0.98\textwidth}")) as table:
            table.add_row(["", textcolor
            (   
            par=False,
            hspace="0mm",
            size="12",
            vspace="14",
            color="gris",
            bold=True,
            text=f"{nomEscue}"
            )])
            table.append(NoEscape('[-4pt]'))
            table.add_row(["", textcolor
            (   
            par=False,
            hspace="0mm",
            size="12",
            vspace="14",
            color="gris",
            bold=True,
            text=f"{strProgr}" 
            )])
    doc.append(NewPage())
    doc.change_document_style("headfoot")
    doc.append(textcolor
            (   
            size="14",
            vspace="0",
            color="parte",
            bold=True,
            text="I parte: Aspectos relativos al plan de estudios"
            ))
    doc.append(textcolor
            (   
            hspace="4mm",
            size="12",
            vspace="20",
            color="parte",
            bold=True,
            text="1 Datos generales"
            ))
    with doc.create(Tabularx(table_spec=r"p{7cm}p{9cm}")) as table:
            table.add_row([bold("Nombre del curso:"), f"{nomCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Código:"), f"{codCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Tipo de curso:"), f"{tipCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Electivo o no:"), f"{eleCurso}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº de créditos:"), f"{numCredi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº horas de clase por semana:"), f"{horClass}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Nº horas extraclase por semana:"), f"{horExtra}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("% de areas curriculares:"), NoEscape(f"{porAreas}" + r'\% del area: ' + bold(f"{areCurso}"))])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Ubicación en el plan de estudios:"), NoEscape(f"{ubiPlane}")])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Requisitos:"), f"{susRequi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Correquisitos:"), f"{corRequi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("El curso es requisito de:"), f"{essRequi}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Asistencia:"), f"{tipAsist}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Suficiencia:"), f"{posSufic}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Posibilidad de reconocimiento:"), f"{posRecon}"])
            table.append(NoEscape('[10pt]'))
            table.add_row([bold("Vigencia del programa:"), f"{vigProgr}"])
            table.append(NoEscape('[10pt]'))
    doc.append(VarCol("2 Descripción general",desGener))
    doc.append(VerticalSpace("10mm", star=True))
    doc.append(VarCol("3 Objetivos",objCurso))
    doc.append(VerticalSpace("10mm", star=True))
    doc.append(VarCol("4 Contenidos",conCursoStr))
    doc.append(VerticalSpace("10mm", star=True))
    doc.append(NewPage())
    doc.append(textcolor
    (   
    size="14",
    vspace="0",
    color="parte",
    bold=True,
    text="II parte: Aspectos operativos"
    ))
    doc.append(textcolor
    (   
    size="12",
    vspace="0",
    color="parte",
    bold=True,
    text=" "
    ))
    with doc.create(LongTabularx(table_spec=r">{\raggedright}p{0.18\textwidth}p{0.72\textwidth}",row_height=1.5)) as table:
            table.add_row([
                textcolor
                (
                size="12",
                vspace="0",
                color="parte",
                bold=True,
                text="5 Metodología de enseñanza y aprendizaje"
                ),
                f"{metCurso}"
            ])
    # doc.append(VarCol("5 Metodología de enseñanza y aprendizaje",metCurso))
    with doc.create(Tabularx(table_spec=r">{\raggedright}m{0.18\textwidth}m{0.07\textwidth}m{0.17\textwidth}m{0.17\textwidth}m{0.17\textwidth}m{0.04\textwidth}")) as table:
            #table.add_hline(start=3, end=5)
            table.add_row([
                textcolor
                (
                size="12",
                vspace="0",
                color="parte",
                bold=True,
                text="6 Evaluación"
                ),
                '',
                textcolor
                (
                size="12",
                vspace="16",
                color="black",
                bold=True,
                text="Tipo"
                ),
                textcolor
                (
                size="12",
                vspace="16",
                color="black",
                bold=True,
                text="Cantidad"
                ),
                textcolor
                (
                size="12",
                vspace="16",
                color="black",
                bold=True,
                text="Porcentaje" 
                ),
                ''
            ])
            table.append(NoEscape('[12pt]'))
            for row in evaCurso.itertuples(index=False):
                #table.add_hline(start=3, end=5)
                table.add_row(row)
                table.append(NoEscape('[12pt]'))
    # with doc.create(LongTabularx(table_spec=r">{\raggedright}p{0.18\textwidth}p{0.72\textwidth}",row_height=1.5)) as table:
    #         table.add_row([
    #             textcolor
    #             (
    #             size="12",
    #             vspace="0",
    #             color="parte",
    #             bold=True,
    #             text="7 Bibliografía"
    #             ),NoEscape(bibCurso)
    #         ])
    doc.append(VarCol("7 Bibliografía",bibCurso))
    doc.append(VerticalSpace("10mm", star=True))
    doc.append(VarCol("8 Profesor",proCurso))
    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex')
    subprocess.run(["biber", "C:\\Repositories\\IEM_programas\\programas\\IEM2101"])
    doc.generate_pdf(f"./programas/{codCurso}", clean=False, clean_tex=False, compiler='lualatex')
    doc.generate_pdf(f"./programas/{codCurso}", clean=True, clean_tex=False, compiler='lualatex') 

# for codigo in cursos.Codigo:
#      generar_programa(codigo)

listProf = ['LCR0','CVS0']
generar_programa("IEM2101",listProf)