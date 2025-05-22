from apiflask import APIBlueprint

bp = APIBlueprint('amenity', __name__, tag="amenity")

from app.blueprints.amenity import routes