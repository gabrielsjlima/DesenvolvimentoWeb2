from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from dao.evento_dao import EventoDAO
from extensions import db
from models.evento import Evento
from models.participante import Participante
from models.inscricao import Inscricao
from security import login_required
from validacao import validar_evento

evento_bp = Blueprint('evento', __name__)

@evento_bp.get('/')
def index():
    return render_template('index.html', eventos=EventoDAO.listar())

@evento_bp.post('/eventos')
@login_required
def cadastrar():
    try:
        EventoDAO.salvar(Evento(**validar_evento(request.form.to_dict())))
        flash('Evento cadastrado com sucesso!', 'sucesso')
    except ValueError as err:
        flash(str(err), 'erro')
    return redirect(url_for('evento.index'))

@evento_bp.route('/eventos/<int:evento_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(evento_id):
    evento = EventoDAO.buscar(evento_id)
    if not evento:
        abort(404)
    if request.method == 'POST':
        try:
            for campo, valor in validar_evento(request.form.to_dict()).items():
                setattr(evento, campo, valor)
            db.session.commit()
            flash('Evento atualizado!', 'sucesso')
            return redirect(url_for('evento.index'))
        except ValueError as err:
            flash(str(err), 'erro')
    return render_template('editar.html', evento=evento)

@evento_bp.post('/eventos/<int:evento_id>/excluir')
@login_required
def excluir(evento_id):
    evento = EventoDAO.buscar(evento_id)
    if not evento:
        abort(404)
    EventoDAO.excluir(evento)
    flash('Evento excluido!', 'sucesso')
    return redirect(url_for('evento.index'))

@evento_bp.post('/eventos/<int:evento_id>/inscrever')
def inscrever(evento_id):
    evento = EventoDAO.buscar(evento_id)
    if not evento:
        abort(404)
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip().lower()
    if not nome or len(nome) > 120 or '@' not in email or len(email) > 255:
        flash('Nome e e-mail validos sao necessarios.', 'erro')
        return redirect(url_for('evento.index'))
    participante = Participante.query.filter_by(email=email).first()
    if participante and Inscricao.query.filter_by(participante_id=participante.id, evento_id=evento.id).first():
        flash('Este participante ja esta inscrito.', 'erro')
        return redirect(url_for('evento.index'))
    total = Inscricao.query.filter_by(evento_id=evento.id).count()
    if total >= (evento.vagas or 0):
        flash('Evento sem vagas disponiveis.', 'erro')
        return redirect(url_for('evento.index'))
    try:
        if not participante:
            participante = Participante(nome=nome, email=email)
            db.session.add(participante)
            db.session.flush()
        db.session.add(Inscricao(participante_id=participante.id, evento_id=evento.id))
        db.session.commit()
        flash('Inscricao realizada com sucesso!', 'sucesso')
    except IntegrityError:
        db.session.rollback()
        flash('Erro: inscricao duplicada.', 'erro')
    return redirect(url_for('evento.index'))
