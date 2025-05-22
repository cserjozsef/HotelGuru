from datetime import datetime
from app.extensions import db
from app.blueprints.invoice.schemas import InvoiceSchema, InvoiceRequestSchema, InvoiceUpdateSchema
from app.models.invoice import Invoice
from sqlalchemy import select

class InvoiceService:

    @staticmethod
    def invoice_list_all():
        invoice = db.session.execute(select(Invoice)).scalars()
        return True, InvoiceSchema().dump(invoice, many=True)

    @staticmethod
    def invoice_add(request):
        try:
            invoice = Invoice(**request)
            db.session.add(invoice)
            db.session.commit()
        except Exception as ex:
            return False, str(ex)
        return True, "Invoice has been added"

    @staticmethod
    def invoice_update(request):
        try:
            invoice = db.session.get(Invoice, request["id"])
            if invoice:
                invoice.date = datetime.strptime(request["date"], '%Y-%m-%d')
                invoice.method = request["method"]
                invoice.amount = request["amount"]
                db.session.commit()
            else:
                return False, "Invoice does not exist"
        except Exception as ex:
            return False, str(ex)
        return True, InvoiceUpdateSchema().dump(invoice)

    @staticmethod
    def invoice_delete(id):
        try:
            invoice = db.session.get(Invoice, id)
            if not invoice:
                return False, "Invoice does not exist"
            elif invoice:
                db.session.delete(invoice)
                db.session.commit()
                return True, "Invoice has been deleted"
        except Exception as ex:
            return False, str(ex)
        return True, "OK"

    @staticmethod
    def invoice_get(id):
        invoice = db.session.get(Invoice, id)
        if not invoice:
            return False, "Invoice does not exist"
        return True, InvoiceSchema().dump(invoice)
