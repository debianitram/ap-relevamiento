from models import *

for col in db_column.executesql('SELECT * FROM markers', as_dict=True):
    Columna.insert(
                altura=col['altura'],
                numero=col['numero'],
                lat=col['lat'],
                lng=col['lng'],
                fecha_registro=col['fecha_registro'],
                tipo=col['tipo'],
                grupo=['grupo'],
                emplazamiento=col['emplazamiento'],
                direccion="%s | %s/ %s" % (col['sobre'], col['interseccion'], col['interseccion2']),
                orden=col['orden'])

db.commit()