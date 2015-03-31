import os

from bottle import route, run
from bottle import request, response, get, post, static_file, redirect
from gluino import wrapper, SQLFORM, current, IS_NOT_EMPTY, Storage

from models import db, Columna, Relevamiento

# Configure the gluino wrapper
wrapper.debug = True
wrapper.redirect = lambda status, url: redirect(url)

current.request = Storage()
current.session = Storage()
current.response = Storage()

# App Bottle
appdir = os.path.dirname(os.path.dirname(__file__))



@get('/')
@post('/')
@wrapper(view='templates/index.html')
def index():
    query = request.query.q
    page = 0 if not request.query.page else int(request.query.page)
    limitby = (page * 1, (page + 1) * 2)

    if query:
        columns = db(Columna.numero == int(query)).select()
    else:
        columns = db(Columna).select(limitby=limitby, orderby=Columna.numero)

    if columns:
        columns = columns[0]

    return dict(query=query, col=columns, page=page)


@post('/form-relevamiento')
def form_relevamiento():
    return dict()


@post('/form-lampara')
def form_lampara():
    return 'resultado'


@route('/columna/add')
@post('/columna/add')
@wrapper(view='templates/columna_add.html', dbs=[db])
def columna_add():
    message = ''
    post_vars = wrapper.extract_vars(request.forms)
    form = SQLFORM(Columna)

    if form.accepts(post_vars):
        message = 'Completo'

    elif form.errors:
        message = 'Error'

    return dict(form=form, message=message)
    


    

@route('/statics/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(appdir, 'statics'))


if __name__ == '__main__':
    run(host='0.0.0.0', port='8080', debug=True, reloader=True)
