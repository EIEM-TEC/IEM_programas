import pandas as pd

mallas = pd.read_csv("mallas_IEM.csv",
    dtype = {'Codigo':str,'Programa':str,'Plan':str,'Semestre':int,'Columna':int,'HorasTeoria':int,'HorasPractica':int,'Creditos':int})

mallas.sort_values(by=['Programa','Semestre','Columna'], ascending=True, inplace=True)


mallas.to_csv('mallas_IEM.csv', index=False, encoding='utf-8-sig')