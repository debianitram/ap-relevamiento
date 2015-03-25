#!/usr/bin/env python

from web2py_dal import DAL, Field

db = DAL('sqlite://databases/storage.db')


Columna = db.define_table('Columna',
                Field('codigo'),
                format='%(codigo)s',
                migrate='databases/Columna.migrate')
