#qpy:webapp:Relevamiento
#qpy://127.0.0.1:8080/

import os
import json

from bottle import route, run, Bottle, ServerAdapter, HTTPResponse
from bottle import request, response, get, post, static_file, redirect
from gluino import wrapper, SPAN, A

from validate import validate
from models import db, Columna, Relevamiento, Lampara

# Configure the gluino wrapper
wrapper.debug = True
wrapper.redirect = lambda status, url: redirect(url)

# App Bottle
appdir = os.path.dirname(os.path.dirname(__file__))

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        import threading
        threading.Thread(target=self.server.shutdown).start()
        self.server.server_close()
        print('# qpyhttpd stop')



@wrapper(view='templates/index.html')
def index():
    query = request.query.q
    page = 0 if not request.query.page else int(request.query.page)
    limitby = (page * 1, (page + 1) * 2)
    relevamiento = False

    if query:
        column = db(Columna.numero == int(query)).select()
    else:
        column = db(Columna).select(limitby=limitby, orderby=Columna.numero)

    if column:
        column = column[0]
        if not column.relevamiento.isempty():
            relevamiento = column.relevamiento.select()[0]

    return dict(query=query, page=page, col=column, relevamiento=relevamiento)



@wrapper()
def form_relevamiento():
    vars = wrapper.extract_vars(request.forms)
    return json.dumps(vars)



def form_lampara():
    values = wrapper.extract_vars(request.forms)
    eval_values = validate(Lampara, values)
    
    if not eval_values:
        lampara = Lampara.insert(**values)
        luz = A(SPAN(_class='glyphicon glyphicon-record'),
                _href='#%s' % lampara.id)
        db.commit()
        return HTTPResponse(luz.xml(), 200)
    
    else:
        return HTTPResponse(json.dumps(eval_values), 500)


@route('/statics/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(appdir, 'statics'))


app = Bottle()
app.route('/', method=['GET', 'POST'])(index)
app.route('/form-lampara', method='POST')(form_lampara)
app.route('/form-relevamiento', method='POST')(form_relevamiento)
app.route('/statics/<filepath:path>', method='GET')(server_static)

try:
    server = MyWSGIRefServer(host='127.0.0.1', port='8080')
    app.run(server=server, reloader=True)
except Exception, ex:
    print('Exception: %s' % repr(ex))