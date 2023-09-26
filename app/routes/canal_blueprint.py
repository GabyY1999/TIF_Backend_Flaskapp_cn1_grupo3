from flask import Blueprint
from ..controllers.canal_controller import CanalController

canal_bp = Blueprint('canal', __name__)
canal_bp.route('/crear_canal', methods=['POST'])(CanalController.crear_canal)
canal_bp.route('/obtener_canales_servidor/<int:servidor_id>', methods=['GET'])(CanalController.obtener_canales_servidor)