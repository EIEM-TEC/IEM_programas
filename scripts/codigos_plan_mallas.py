import pandas as pd

mallas = pd.read_csv("mallas_IEM.csv")

def codigos(programa):
    match programa:
        case 'AeronáuticaV1':
            return 'AE','0001'
        case 'AeronáuticaV2':
            return 'AE','0002'
        case 'Mantenimiento Industrial':
            return 'MI','1313'
        case 'Electromecánica':
            return 'EM','0001'

result = mallas.apply(lambda x: codigos(x['Programa']), axis=1, result_type='expand')

print(result)


neworder = ['Codigo','Programa','Plan','Area','Semestre','Columna','HorasTeoria','HorasPractica','Creditos']
mallas_new = mallas.join(result)\
    .rename(columns={0: 'codPrograma', 1: 'Plan'})\
    .drop('Programa',axis=1)\
    .rename(columns={'codPrograma':'Programa'})\
    .reindex(columns=neworder)

print(mallas_new)

mallas_new.to_csv('mallas_IEM.csv', index=False, encoding='utf-8-sig')