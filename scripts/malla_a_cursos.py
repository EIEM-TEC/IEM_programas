import pandas as pd

mallas = pd.read_csv("mallas_IEM.csv")
cursos = pd.read_csv("cursos_IEM.csv")

# print(mallas)
# print(cursos)

all = mallas.merge(cursos.drop_duplicates(), on=['Codigo','Nombre'],
                   how='left', indicator=True)[['Codigo','Nombre','_merge']]
mallas_only = all[all['_merge'] == 'left_only']

cursos_new = pd.concat([cursos,mallas_only]).drop('_merge', axis=1)

print(cursos_new)

cursos_new.to_csv('cursos_IEM.csv', index=False, encoding='utf-8-sig')