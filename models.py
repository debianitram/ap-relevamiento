#!-*- encoding:utf-8 -*-

from gluino import DAL, Field
from gluino import IS_NOT_EMPTY, IS_EMPTY_OR, IS_IN_DB

db = DAL('sqlite://databases/storage.db')

ASPECTO = ('', 'Despintada', 'Sucia', 'Otro')
ESTADO = ('', 'Excelente', 'Bueno', 'Malo')
INVACION = ('', 'Árbol', 'Cartel', 'Cable', 'Todo')
ALIMENTACION = ('', 'Aerea', 'Subterranea')
ENCENDIDO = ('', 'E/E', 'Foto Célula')
TIPO_COLUMNA = ('', 'Poste', 'Hormigon', 'Hierro')

OPCIONES = {'aspecto': ASPECTO,
            'estado': ESTADO,
            'invacion': INVACION,
            'alimentacion': ALIMENTACION,
            'encendido': ENCENDIDO,
            'tipo_columna': TIPO_COLUMNA}

mg = True

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
                migrate='databases/Columna.migrate' if mg else False,
                )


Relevamiento = db.define_table('relevamiento',
                Field('columna', Columna), 
                Field('tipo_soporte', requires=IS_NOT_EMPTY()),
                Field('color'),
                Field('propio', 'boolean', default=True),
                Field('aspecto', requires=IS_NOT_EMPTY()),
                Field('estado', requires=IS_NOT_EMPTY()),
                Field('tapa_inspeccion', 'boolean'),
                Field('puntos_luz', 'integer', default=0),
                Field('imagen', 'upload'),
                Field('invadida', requires=IS_NOT_EMPTY()),
                Field('observacion_piquete'),
                Field('tipo_alimentacion', requires=IS_NOT_EMPTY()),
                Field('sistema_encendido', requires=IS_NOT_EMPTY()),
                Field('observacion_alimentacion', 'text'),
                format='%(columna)s',
                migrate='databases/Relevamiento.migrate' if mg else False,
                )

Lampara = db.define_table('lampara',
                Field('relevamiento',
                      Relevamiento,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, Relevamiento))),
                Field('tipo'),
                Field('estado', requires=IS_NOT_EMPTY()),
                Field('modelo_artefacto'),
                Field('potencia', 'integer', requires=IS_NOT_EMPTY()),
                format='%(id)s: %(potencia)s W',
                migrate='databases/Lampara.migrate' if mg else False,
                )