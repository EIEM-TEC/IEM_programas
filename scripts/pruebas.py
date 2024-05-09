import pandas as pd
import numpy as np

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

codigo = "IEM2101"
codCurso = codigo
lisProgr = cursos[cursos.Codigo == codCurso].Programas.str.split('\n',expand=False).explode()
lisProgr = lisProgr.str.split(';',expand=True)
lisProgr.reset_index(inplace = True, drop = True)
lisProgr.columns = ['programa','semestre']

objGener = descrip_obj[descrip_obj.Codigo == codCurso].ObjetivoGeneral.item()
objGener = objGener[0].lower() + objGener[1:len(objGener)]
print(objGener)


if len(lisProgr) > 1:
    strProgr = "Carreras de: " + ' e'.join(lisProgr['programa'].str.cat(sep='; ').rsplit(';',1))
else:
    strProgr = "Carrera de " + lisProgr['programa'].item()

print(np.sort(lisProgr['semestre'].unique()))
ubiPlane = ""
for sem in np.sort(lisProgr['semestre'].unique()):
    filter = lisProgr["semestre"] == str(sem)
    filterlist = lisProgr[filter]
    print(filterlist)
    ubiPlane += "Curso de "
    ubiPlane += number_to_ordinals(str(sem))
    ubiPlane += " semestre en "
    if len(filterlist)  > 1:
        ubiPlane += ' e'.join(filterlist['programa'].str.cat(sep='; ').rsplit(';',1)) + ". "
    else:
        ubiPlane += filterlist['programa'].item() + ". "

        
#         for index, row in filterlist.iterrows():
#             ubiPlane += row["programa"]
#             fila += 1
#             if fila == shape:
#                 ubiPlane += ". "
#             elif fila == shape - 1:
#                 ubiPlane += " e "              
#             else:
#                 ubiPlane += "; "


print(ubiPlane)



# print(lisProgr.groupby('semestre')['programa'].transform('all'))
# print(lisProgr.groupby(['semestre']).max())
# print(lisProgr.sort_values(['semestre']).set_index(['semestre']))


# for sem in range(1,int(lisProgr["semestre"].max())+1):
#     filter = lisProgr["semestre"] == str(sem)
#     filterlist = lisProgr[filter]
#     shape = filterlist.shape[0]
#     if shape  != 0:
#         ubiPlane += "Curso de "
#         ubiPlane += number_to_ordinals(str(sem))
#         ubiPlane += " semestre en "
#         fila = 0
#         for index, row in filterlist.iterrows():
#             ubiPlane += row["programa"]
#             fila += 1
#             if fila == shape:
#                 ubiPlane += ". "
#             elif fila == shape - 1:
#                 ubiPlane += " e "              
#             else:
#                 ubiPlane += "; "



contenidos = pd.DataFrame()
contenidos = descrip_obj[descrip_obj.Codigo == codCurso].Contenidos.str.split('\r\n',expand=False).explode()
contenidos.reset_index(inplace = True, drop = True)
nivel_1, nivel_2, nivel_3 = [0,0,0]
for index, row in contenidos.items():
    res = 0
    for pos in range(3):
        if pos == row.find('*', pos, pos+1):
            res += 1
    if res == 1:
        nivel_1 += 1
        nivel_2 = 0
        contenidos.iloc[index] = row.replace('*', f"{str(nivel_1)} ")
    elif res == 2:
        nivel_2 += 1
        nivel_3 = 0
        contenidos.iloc[index] = row.replace('**', f"  {str(nivel_1)}.{str(nivel_2)} ")
    elif res == 3:
        nivel_3 += 1
        contenidos.iloc[index] = row.replace('***', f"    {str(nivel_1)}.{str(nivel_2)}.{str(nivel_3)} ")

objGener = descrip_obj[descrip_obj.Codigo == codCurso].ObjetivoGeneral.item()

objEspec = descrip_obj[descrip_obj.Codigo == codCurso].ObjetivosEspecificos.str.split('\n',expand=False).explode()
objEspec.reset_index(inplace = True, drop = True)
#print(objEspec)



