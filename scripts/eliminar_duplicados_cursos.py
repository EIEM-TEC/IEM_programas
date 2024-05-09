import pandas as pd




cursos = pd.read_csv("cursos_IEM.csv")
cursos.drop_duplicates('Codigo', inplace=True)


cursos.sort_values(by=['Codigo'], ascending=True, inplace=True)


cursos.to_csv('cursos_IEM.csv', index=False, encoding='utf-8-sig')