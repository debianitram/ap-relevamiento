#!-*- encoding:utf-8 -*-

from gluino import DAL, Field
from gluino import IS_NOT_EMPTY, IS_EMPTY_OR, IS_IN_DB

db = DAL('sqlite://databases/storage.db', pool_size=1)


ESTADO = ('', 'Excelente', 'Bueno', 'Malo')
ACOMETIDA = ('', 'Aerea', 'Subterranea')
SOSTEN = ('', 'Columna', 'Madera', 'HA')
PUESTA_TIERRA = ('', 'Si', 'No', 'Discontinua')

OPCIONES = {'estado': ESTADO,
            'acometida': ACOMETIDA,
            'sosten': SOSTEN,
            'pt': PUESTA_TIERRA}


Columna = db.define_table('columna',
                Field('numero', length=50, requires=IS_NOT_EMPTY()),
                Field('lat', 'float'),
                Field('lng', 'float'),
                Field('fecha_registro', 'datetime'),
                Field('tipo', length=30),
                Field('eliminado', 'integer'),
                Field('grupo', length=30),
                Field('procesado', 'integer'),
                Field('emplazamiento', length=50),
                Field('direccion'),
                Field('altura'),
                Field('orden', 'integer'),
                format='%(numero)s',
                migrate='databases/Columna.migrate',
                )


Relevamiento = db.define_table('relevamiento',
                Field('columna', Columna), 
                Field('sosten', requires=IS_NOT_EMPTY()),
                Field('color', 'string', length=50),
                Field('base_oxido', 'boolean'),
                Field('base_sello', 'boolean'),
                Field('base_madera', 'string', length=50),
                Field('boca_inspeccion', 'boolean'),
                Field('sujecion_brazo', 'string', length=20),
                Field('acometida', 'string', length=250),
                Field('puesta_tierra', 'string', length=50),
                Field('puntos_luz', 'integer', default=0),
                Field('imagen', 'upload'),
                Field('observacion_piquete'),
                Field('observacion_sosten', 'text'),
                Field('observacion_luminaria', 'text'),
                format='%(columna)s',
                migrate='databases/Relevamiento.migrate',
                )


Lampara = db.define_table('luminaria',
                Field('relevamiento',
                      Relevamiento,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, Relevamiento))),
                Field('tipo', 'string', length=200),
                Field('estado', requires=IS_NOT_EMPTY()),
                Field('modelo_artefacto'),
                Field('potencia', 'integer', requires=IS_NOT_EMPTY()),
                Field('tulipa', 'string'),
                Field('proteccion', 'string', length=50),
                format='%(id)s: %(potencia)s W',
                migrate='databases/Lampara.migrate',
                )