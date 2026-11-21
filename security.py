import functools
import secrets
from flask import flash, jsonify, redirect, request, session, url_for
from extensions import db
from models.usuario import Usuario

def csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(24)
    return session['_csrf_token']

def usuario_atual():
    uid = session.get('usuario_id')
    return db.session.get(Usuario, uid) if uid else None

def login_required(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        if not usuario_atual():
            if request.path.startswith('/api/'):
                return jsonify({'erro':'Autenticacao necessaria.'}), 401
            flash('Entre para continuar.', 'erro')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)
    return wrapped
