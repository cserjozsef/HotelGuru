from apiflask import APIBlueprint

bp = APIBlueprint('booking', __name__, tag="booking")

from app.blueprints.booking import routes