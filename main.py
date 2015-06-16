#qpy:2

import os
import md5
import json

from core import validate, select
from models import db, Columna, Relevamiento, Lampara, index_aux
from models import APP_DIR, FOLDER_STATICS, FOLDER_UPLOAD, FOLDER_TEMPLATES

from bottle import route, run, Bottle, ServerAdapter, HTTPResponse
from bottle import request, response, get, post, static_file, redirect
from gluino import wrapper, SPAN, A, LI, INPUT

# Configure the gluino wrapper
wrapper.debug = True
wrapper.redirect = lambda status, url: redirect(url)

# Templates
T_INDEX = os.path.join(FOLDER_TEMPLATES, 'index.html')
T_LAYOUT = os.path.join(FOLDER_TEMPLATES, 'layout.html')
T_ADD_LAMPARA = os.path.join(FOLDER_TEMPLATES, 'lampara-add.html')

templates = {'index': T_INDEX,
             'layout': T_LAYOUT,
             'lampara': T_ADD_LAMPARA}
# App Bottle


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



######### BUILT-IN ROUTERS ###############
@route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@route('/__ping')
def __ping():
    return "ok"



@wrapper(view=templates.get('index'))
def index():
    query = request.query.q
    page = 0 if not request.query.page else int(request.query.page)
    limitby = (page * 1, (page + 1))
    
    relevamiento = False
    pre_relevamiento = False

    if query:
        column = db(Columna.numero == int(query)).select()
    else:
        column = db(Columna).select(limitby=limitby, orderby=Columna.numero)
        

    if column:
        column = column[0]
        if not column.relevamiento.isempty():
            relevamiento = column.relevamiento.select()[0]
        
        else:
            if page:
                newlimit = ((page -1) * 1, page)
                prev = db(Columna).select(limitby=newlimit,
                                          orderby=Columna.numero).first()
                if column.relevamiento.isempty() and not prev.relevamiento.isempty():
                    pre_relevamiento = prev.relevamiento.select().first()

    return dict(query=query,
                page=page,
                col=column,
                relevamiento=relevamiento,
                pre_relevamiento=pre_relevamiento,
                fn_select=select,
                templates=templates
                )



def form_relevamiento():

    vars = wrapper.extract_vars(request.forms)
    vars.update(base_oxido=vars.get('base_oxido', False))
    vars.update(base_sello=vars.get('base_sello', False))
    vars.update(boca_inspeccion=vars.get('boca_inspeccion', False))
    vars.update(tapa_inspeccion=vars.get('tapa_inspeccion', False))
    vars.update(necesita_poda=vars.get('necesita_poda', False))
    vars.update(intervencion_inmediata=vars.get('intervencion_inmediata', False))

    page = vars.pop('page')

    relevamiento_id = vars.pop('relevamiento_id')

    relevamiento = Relevamiento.update_or_insert(
        Relevamiento.id == relevamiento_id, **vars)

    if relevamiento or relevamiento_id:
        
        r = Relevamiento(relevamiento.id if relevamiento else relevamiento_id)

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
    return static_file(filepath, root=FOLDER_STATICS)


def upload_static(filepath):
    return static_file(filepath, root=FOLDER_UPLOAD)


def upload_imagen():
    image = request.forms.get('imagen1') or \
             request.forms.get('imagen2') or \
             request.forms.get('imagen3')

    relevamiento = int(request.forms.relevamiento)
    image_id = request.forms.get('id')
    
    if not relevamiento:
        return HTTPResponse(json.dumps(
            {'error': 'Debe cargar el relevamiento primero'}), 406)

    if image:
        r = Relevamiento(relevamiento)
        expression = {image_id: image}
        r.update_record(**expression)

        return HTTPResponse(json.dumps({'id': image_id, 'image': image}), 200)



######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method=['GET', 'POST'])(index)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/form-lampara', method='POST')(form_lampara)
app.route('/form-relevamiento', method='POST')(form_relevamiento)
app.route('/upload-image', method='POST')(upload_imagen)
app.route('/delete_item', method='GET')(delete_item)
app.route('/statics/<filepath:path>', method='GET')(server_static)
app.route('/upload/<filepath:path>', method='GET')(upload_static)

try:
    server = MyWSGIRefServer(host='localhost', port='8080')
    app.run(server=server, reloader=True)

except Exception, ex:
    print('Exception: %s' % repr(ex))