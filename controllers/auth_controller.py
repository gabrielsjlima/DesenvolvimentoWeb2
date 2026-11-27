from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.usuario import Usuario
from security import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        if not nome or len(nome) > 120 or not email or '@' not in email or len(email)>255 or len(senha) < 8:
            flash('Informe nome, e-mail valido e senha com pelo menos 8 caracteres.', 'erro')
        elif Usuario.query.filter_by(email=email).first():
            flash('Este e-mail ja foi cadastrado.', 'erro')
        else:
            novo = Usuario(nome=nome, email=email)
            novo.definir_senha(senha)
            try:
                db.session.add(novo)
                db.session.commit()
                flash('Conta criada! Faca login.', 'sucesso')
                return redirect(url_for('auth.login'))
            except IntegrityError:
                db.session.rollback()
                flash('E-mail ja cadastrado.', 'erro')
    return render_template('cadastro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_senha(senha):
            session.clear()
            session['usuario_id'] = usuario.id
            flash('Login realizado!', 'sucesso')
            return redirect(url_for('evento.index'))
        flash('E-mail ou senha incorretos.', 'erro')
    return render_template('login.html')

@auth_bp.post('/logout')
@login_required
def logout():
    session.clear()
    flash('Voce saiu da conta.', 'sucesso')
    return redirect(url_for('evento.index'))
