#!-*- encoding:utf-8 -*-

from gluino import DAL, Field, IS_NOT_EMPTY

db = DAL('sqlite://databases/storage.db')
db_column = DAL('mysql://root:mysql123@localhost/gpsd')

ASPECTO = ('Despintada', 'Sucia', 'Otro')
ESTADO = ('Excelente', 'Bueno', 'Malo')
INVACION = ('Árbol', 'Cartel', 'Cable', 'Todo')
ALIMENTACION = ('Aerea', 'Subterranea')
ENCENDIDO = ('E/E', 'Foto Célula')

Columna = db.define_table('Columna',
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

Soporte = db.define_table('columna_soporte',
                Field('nombre'),
                format='%(nombre)s',
                migrate='databases/Soporte.migrate')


Relevamiento = db.define_table('relevamiento',
                Field('columna', Columna), 
                Field('tipo_soporte', Soporte),
                Field('color'),
                Field('propio', 'boolean', default=True),
                Field('aspecto'),
                Field('estado'),
                Field('tapa_inspeccion', 'boolean'),
                Field('puntos_luz', 'integer', default=0),
                Field('imagen', 'upload'),
                Field('invadida'),
                Field('observacion_piquete'),
                Field('tipo_alimentacion'),
                Field('sistema_encendido'),
                Field('observacion_alimentacion', 'text'),
                format='%(columna)s',
                migrate='databases/Relevamiento.migrate'
                )

Lampara = db.define_table('lampara',
                Field('relevamiento', Relevamiento),
                Field('tipo'),
                Field('estado', 'list:string'),
                Field('modelo_artefacto', 'list:string'),
                Field('potencia', 'integer'),
                format='%(nombre)s: %(potencia)s W',
                migrate='databases/Lampara.migrate')