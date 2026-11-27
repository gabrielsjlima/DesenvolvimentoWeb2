import os
import secrets
from pathlib import Path
from flask import Flask, jsonify, request, session
from extensions import db

def create_app(test_config=None):
    app = Flask(__name__)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(Path(app.instance_path) / 'eventos.db')
    if database_url.startswith(('postgres://', 'postgresql://')):
        database_url = 'postgresql+psycopg://' + database_url.split('://', 1)[1]
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        SQLALCHEMY_DATABASE_URI=database_url,
        SESSION_COOKIE_SECURE=os.environ.get('RENDER') == 'true',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    from models.evento import Evento
    from models.participante import Participante
    from models.inscricao import Inscricao
    from models.usuario import Usuario
    from controllers.evento_controller import evento_bp
    from controllers.auth_controller import auth_bp
    from controllers.api_controller import api_bp
    from security import csrf_token, usuario_atual
    app.register_blueprint(evento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def template_variables():
        return {'csrf_token': csrf_token, 'usuario_atual': usuario_atual()}

    @app.before_request
    def verify_csrf():
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token', '')
            if not token or not secrets.compare_digest(token, session.get('_csrf_token', '')):
                if request.path.startswith('/api/'):
                    return jsonify({'erro': 'Token CSRF ausente ou invalido.'}), 400
                from flask import abort
                abort(400, description='Formulário expirado; atualize a página.')

    with app.app_context():
        db.create_all()
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
