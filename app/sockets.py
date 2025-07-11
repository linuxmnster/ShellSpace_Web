from flask_socketio import emit

def register_socketio(socketio):
    @socketio.on('message')
    def handle_message(msg):
        emit('message', msg, broadcast=True)
