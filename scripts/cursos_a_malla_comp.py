import pandas as pd
import numpy as np

cursos = pd.read_csv("cursos_IEM.csv")
mante = pd.read_csv("mantenimiento.csv")
elect = pd.read_csv("electromecanica.csv")
aer1 = pd.read_csv("aeronauticaV1.csv")
aer2 = pd.read_csv("aeronauticaV2.csv")

mallas = pd.concat([mante,elect,aer1,aer2])
mallas.reset_index(inplace = True, drop = True)

mallas['Compartido'] = ""

mallascomp1 = mallas.loc[(mallas.Programa == "AeronáuticaV2") | (mallas.Programa == "Electromecánica")]
mallascomp2 = mallas.loc[(mallas.Programa == "AeronáuticaV1") | (mallas.Programa == "Mantenimiento Industrial")]

counts1 = mallascomp1.Codigo.value_counts()
counts2 = mallascomp2.Codigo.value_counts()

for codigo in mallascomp1.Codigo:
    if counts1[counts1.index == codigo].item() > 1:
        mallascomp1.loc[mallascomp1.Codigo == codigo, 'Compartido'] = "SI"
    else:
        mallascomp1.loc[mallascomp1.Codigo == codigo, 'Compartido'] = "NO"

for codigo in mallascomp2.Codigo:
    if counts2[counts2.index == codigo].item() > 1:
        mallascomp2.loc[mallascomp2.Codigo == codigo, 'Compartido'] = "SI"
    else:
        mallascomp2.loc[mallascomp2.Codigo == codigo, 'Compartido'] = "NO"

mallascomp = pd.concat([mallascomp1,mallascomp2])

mallascomp.to_csv('mallas_IEM_comp.csv', index=False, encoding='utf-8-sig')