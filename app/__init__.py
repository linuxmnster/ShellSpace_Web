from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace_this_with_random_string'

    from .routes import main
    from .sockets import register_socketio

    app.register_blueprint(main)
    register_socketio(socketio)

    return app
