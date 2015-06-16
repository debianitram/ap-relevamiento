#!-*- encoding:utf-8 -*-
import os
import sys

from gluino import DAL, Field
from gluino import IS_NOT_EMPTY, IS_EMPTY_OR, IS_IN_DB

print ('#######  Cargando ...')

system = 'desktop'

if system == 'desktop':
    APP_DIR = os.getcwd()
    FOLDER_UPLOAD = os.path.join(os.getcwd(), 'upload')
else:
    sys.path.append('/data/data/com.hipipal.qpyplus/files/lib/python2.7/site-packages/bottle-0.12.8-py2.7.egg/')
    APP_DIR = '/sdcard/com.hipipal.qpyplus/projects/Relevamiento'
    FOLDER_UPLOAD = '/sdcard/upload_relevamiento'
# CONFIG PATH

DBPATH = os.path.join(APP_DIR, 'databases/storage.db')

FOLDER_STATICS = os.path.join(APP_DIR, 'statics')
FOLDER_TEMPLATES = os.path.join(APP_DIR, 'templates')


ESTADO = ('', 'Excelente', 'Bueno', 'Malo')
ACOMETIDA = ('', 'Aerea', 'Subterranea')
SOSTEN = ('', 'Columna', 'Madera', 'HA')
PUESTA_TIERRA = ('', 'Si', 'No', 'Discontinua')
TIPO_LAMPARA = ('',
                'SAP 100',
                'SAP 150',
                'SAP 250',
                'SAP 400',
                'ML E27',
                'ML E40',)
MODELO = ('',
          'SIEMENS 5NA 378, hasta 400W',
          'MODELO I',
          'MODELO II')

OPCIONES = {'estado': ESTADO,
            'acometida': ACOMETIDA,
            'sosten': SOSTEN,
            'pt': PUESTA_TIERRA,
            'tp_lampara': TIPO_LAMPARA,
            'modelo': MODELO}


db = DAL('sqlite://%s' % DBPATH, pool_size=1)


Columna = db.define_table('columna',
                Field('numero', 'integer', requires=IS_NOT_EMPTY()),
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
                migrate=os.path.join(APP_DIR, 'databases/Columna.migrate'),
                )


Relevamiento = db.define_table('relevamiento',
                Field('columna', Columna), 
                Field('sosten', requires=IS_NOT_EMPTY()),
                Field('color', 'string', length=50),
                Field('base_oxido', 'boolean'),
                Field('base_sello', 'boolean'),
                Field('base_madera', 'string', length=50),
                Field('boca_inspeccion', 'boolean'),
                Field('columna_reacondicionada', 'boolean'),
                Field('sujecion_brazo', 'string', length=20),
                Field('acometida', 'string', length=250),
                Field('puesta_tierra', 'string', length=50),
                Field('puntos_luz', 'integer', default=0),
                Field('imagen1', 'string', length=250),
                Field('imagen2', 'string', length=250),
                Field('imagen3', 'string', length=250),
                Field('necesita_poda', 'boolean'),
                Field('observacion_sosten', 'text'),
                Field('observacion_luminaria', 'text'),
                Field('destacar', 'boolean'),
                Field('intervencion_inmediata', 'boolean'),
                format='%(columna)s',
                migrate=os.path.join(APP_DIR, 'databases/Relevamiento.migrate'),
                )


Lampara = db.define_table('luminaria',
                Field('columna',
                      Columna,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, Columna))),
                Field('tipo', 'string', length=200),
                Field('estado', requires=IS_NOT_EMPTY()),
                Field('modelo_artefacto'),
                Field('recambio_tulipa', 'boolean'),
                Field('limpieza_tulipa', 'boolean'),
                format='%(id)s: %(potencia)s W',
                migrate=os.path.join(APP_DIR, 'databases/Lampara.migrate'),
                )


index_aux = [i.numero for i in db(Columna).select(orderby=Columna.numero)]
