import pandas as pd
import numpy as np

cursos = pd.read_csv("cursos_IEM.csv")
mante = pd.read_csv("mantenimiento.csv")
elect = pd.read_csv("electromecanica.csv")
aer1 = pd.read_csv("aeronauticaV1.csv")
aer2 = pd.read_csv("aeronauticaV2.csv")

mallas = pd.concat([mante,elect,aer1,aer2])
mallas.reset_index(inplace = True, drop = True)

print(mallas)

for codigo in cursos.Codigo:
    mallas.loc[mallas.Codigo == codigo, 'Nombre'] = cursos[cursos.Codigo == codigo].Nombre.item()

mallas.to_csv('mallas_IEM.csv', index=False, encoding='utf-8-sig')