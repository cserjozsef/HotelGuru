from apiflask import APIBlueprint


bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return 'This is The Main Blueprint'

from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.models import *