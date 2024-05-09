import pandas as pd



cursos = pd.read_csv("cursos_IE.csv")

cursos['mover'] = cursos.apply(lambda row: row.HorasTeoria + row.HorasPractica, axis=1) #nueva columna "mover"
cursos.insert(9, "HorasClase", cursos.mover) # copiar la columna "mover" y cambiarle el nombre
cursos.drop('mover', axis=1, inplace=True) # borrar la columna mover

cursos['mover'] = cursos.apply(lambda row: row.Creditos*3 - row.HorasClase, axis=1)
cursos.insert(10, "HorasExtraclase", cursos.mover)
cursos.drop('mover', axis=1, inplace=True)

areas = cursos.groupby('Area')[['Creditos', 'HorasTeoria', 'HorasPractica', 'HorasClase', 'HorasExtraclase']].sum().reset_index() # sumar creditos por area y convertir el index en columna
print(areas)

cursos['mover'] = 0
for area in areas.Area:
    cursos['mover'] = cursos['mover'] + round(100 * (cursos.Area == area) * (cursos.Creditos) / areas[areas.Area == area].Creditos.item(),1) #calcular porcentaje que cada curso aporta en el area
cursos.insert(11, "AreasCurriculares", cursos.mover)
cursos.drop('mover', axis=1, inplace=True)

cursos.to_csv('datos_IE.csv', index=False,encoding='utf-8-sig' )
areas.to_csv('areas_IE.csv', index=False,encoding='utf-8-sig')

print(cursos.head())

