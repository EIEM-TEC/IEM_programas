import pandas as pd

mallas = pd.read_csv("mallas_IEM.csv")
mallas_new = mallas.drop('Nombre', axis=1)


mallas_new.sort_values(by=['Codigo'], ascending=True, inplace=True)


mallas_new.to_csv('mallas_IEM.csv', index=False, encoding='utf-8-sig')