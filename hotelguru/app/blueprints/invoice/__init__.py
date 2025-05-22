from apiflask import APIBlueprint

bp = APIBlueprint('invoice', __name__, tag="invoice")

from app.blueprints.invoice import routes