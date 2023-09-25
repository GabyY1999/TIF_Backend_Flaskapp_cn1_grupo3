from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from ..controllers.auth_controlller import UserController  # Importa el controlador

auth = Blueprint('auth', __name__)

auth.route('/login', methods=['GET', 'POST'])(UserController.login)
auth.route('/register', methods=['GET', 'POST'])(UserController.register)
auth.route('/welcome')(UserController.welcome)