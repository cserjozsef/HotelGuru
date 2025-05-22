from app.blueprints import role_required
from app.blueprints.invoice import bp
from app.blueprints.invoice.schemas import InvoiceSchema, InvoiceUpdateSchema, InvoiceRequestSchema
from app.blueprints.invoice.service import InvoiceService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Invoice Blueprint'


@bp.post('/add')
@bp.input(InvoiceRequestSchema, location="json")
#@bp.auth_required(auth)
def invoice_add(json_data):
    success, response = InvoiceService.invoice_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(InvoiceUpdateSchema, location="json")
@bp.output(InvoiceSchema)
#@bp.auth_required(auth)
def invoice_update(json_data):
    success, response = InvoiceService.invoice_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def invoice_delete(id):
    success, response = InvoiceService.invoice_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(InvoiceSchema)
#@bp.auth_required(auth)
def invoice_get(id):
    success, response = InvoiceService.invoice_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(InvoiceSchema(many=True))
#@bp.auth_required(auth)
def invoice_list_all():
    success, response = InvoiceService.invoice_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
