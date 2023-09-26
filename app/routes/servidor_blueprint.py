from flask import Blueprint
from ..controllers.servidor_controller import ServidoresController

servidor_bp = Blueprint('servidor', __name__)

servidor_bp.route('/explorar_servidores', methods=['GET'])(ServidoresController.mostrar_todos_servidores)
servidor_bp.route('/unirse_a_servidor/<int:servidor_id>', methods=['POST'])(ServidoresController.unirse_a_servidor)
#servidor_bp.route('/servidores/<int:servidor_id>', methods=['GET'])(ServidoresController.mostrar_servidor)
servidor_bp.route('/crear_servidor', methods=['POST'])(ServidoresController.crear_servidor)
#servidor_bp.route('/servidores/<int:servidor_id>', methods=['DELETE'])(ServidoresController.eliminar_servidor)
servidor_bp.route('/obtener_servidores_usuario/<int:user_id>', methods=['GET'])(ServidoresController.obtener_servidores_usuario)
