from bottle import Bottle, run, request, get, post, static_file, redirect
from gluino import wrapper, SQLFORM, cache, IS_NOT_EMPTY
from gluino import DAL, Field

# Configure the gluino wrapper
wrapper.debug = True
wrapper.redirect = lambda status, url: redirect(url)

# App Bottle
# app = Bottle()


# Create datebase and table
db = DAL('sqlite://databases/test.sqlite')
db.define_table('test',
                Field('name', requires=IS_NOT_EMPTY()),
                migrate='databases/test.migrate',
                format='%(name)s')

# @app.route('/hello')
@get('/index')
@post('/index')
@wrapper(view='templates/index.html', dbs=[db])
def index():
    vars = wrapper.extract_vars(request.forms)
    form = SQLFORM(db.test)
    if form.accepts(vars):
        message = 'Hola %s' % form.vars.name
        
    else:
        message = 'Hola anonimo'
        
    people = db(db.test).select()
    return locals()
    
 

if __name__ == '__main__':
    run(host='localhost', port='8080', debug=True)
