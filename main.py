#qpy:webapp:Relevamiento
#qpy://127.0.0.1:8080/

import os
import md5
import json

from bottle import route, run, Bottle, ServerAdapter, HTTPResponse
from bottle import request, response, get, post, static_file, redirect

from wrapper import wrapper
from gluon import SPAN, A, LI, INPUT

from core import validate, select
from models import db, Columna, Relevamiento, Lampara, index_aux


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

    return dict(query=query,
                page=page,
                col=column,
                relevamiento=relevamiento,
                fn_select=select)



def form_relevamiento():
    vars = wrapper.extract_vars(request.forms)
    vars.update(base_oxido=vars.get('base_oxido', False))
    vars.update(base_sello=vars.get('base_sello', False))
    vars.update(boca_inspeccion=vars.get('boca_inspeccion', False))

    page = vars.pop('page')
    
    images = [request.files.get('imagen1'),
              request.files.get('imagen2'),
              request.files.get('imagen3')]

    for k in range(1, 4):
        key = 'imagen%s' % k
        if vars.has_key(key):
            vars.pop(key)

    relevamiento_id = vars.pop('relevamiento_id')

    relevamiento = Relevamiento.update_or_insert(
        Relevamiento.id == relevamiento_id, **vars)

    if relevamiento or relevamiento_id:
        
        r = Relevamiento(relevamiento.id if relevamiento else relevamiento_id)
        expression = {}
        
        for count, image in enumerate(images):
            
            if not image:
                continue
            
            count += 1
            key = 'imagen%s' % count
            name_image = '%s_%s.jpg' % (md5.new(str(r.id)).hexdigest(), count)
            
            expression.update({key: name_image})

            im = image.save('upload/%s' % name_image,
                             overwrite=True,
                             chunk_size=100000)

        r.update_record(**expression)

    db.commit()
    redirect('/?page=%s' % index_aux.index(r.columna.numero))
    


def form_lampara():
    values = wrapper.extract_vars(request.forms)
    eval_values = validate(Lampara, values)
    
    if not eval_values:
        lampara = Lampara.insert(**values)
        luz = LI(SPAN(_class='glyphicon glyphicon-plus'),
                 ' Tipo: %s | Estado: %s | Proteccion: %s' % (
                                                            lampara.tipo,
                                                            lampara.estado,
                                                            lampara.recambio_tulipa),
                 A(SPAN(_class='glyphicon glyphicon-remove'),
                   _class='btn btn-xs btn-danger remove-item'),
                _class='list-group-item',
                **{'_data-target': 'luminaria-%s' % lampara.id,
                   '_data-db': 'true'})
        db.commit()
        
        return HTTPResponse(luz.xml(), 200)
    
    else:
        return HTTPResponse(json.dumps(eval_values), 500)


def delete_item():
    table, id = request.query.target.split('-')
    registro = db[table][id]
    if registro.delete_record():
        db.commit()
        message = 'Se elimino correctamente'
    else:
        message = 'Error al eliminar el registro %s->%s' % (table, id)
    return message


def server_static(filepath):
    return static_file(filepath, root=os.path.join(appdir, 'statics'))


def upload_static(filepath):
    return static_file(filepath, root=os.path.join(appdir, 'upload'))


app = Bottle()
app.route('/', method=['GET', 'POST'])(index)
app.route('/form-lampara', method='POST')(form_lampara)
app.route('/form-relevamiento', method='POST')(form_relevamiento)
app.route('/delete_item', method='GET')(delete_item)
app.route('/statics/<filepath:path>', method='GET')(server_static)
app.route('/upload/<filepath:path>', method='GET')(upload_static)

try:
    server = MyWSGIRefServer(host='0.0.0.0', port='8080')
    app.run(server=server, reloader=True)
except Exception, ex:
    print('Exception: %s' % repr(ex))