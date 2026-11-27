import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from flask import Blueprint, jsonify, request
from dao.evento_dao import EventoDAO
from extensions import db
from models.evento import Evento
from security import login_required
from validacao import validar_evento

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/eventos')
def listar():
    return jsonify([e.para_dict() for e in EventoDAO.listar()])

@api_bp.get('/eventos/<int:evento_id>')
def buscar(evento_id):
    e = EventoDAO.buscar(evento_id)
    return jsonify(e.para_dict()) if e else (jsonify({'erro':'Evento nao encontrado.'}), 404)

@api_bp.post('/eventos')
@login_required
def criar():
    if not request.is_json:
        return jsonify({'erro':'Envie JSON.'}), 415
    try:
        dados = validar_evento(request.get_json(silent=True))
    except ValueError as err:
        return jsonify({'erro':str(err)}), 400
    e = EventoDAO.salvar(Evento(**dados))
    resposta = jsonify(e.para_dict())
    resposta.status_code = 201
    resposta.headers['Location'] = '/api/eventos/' + str(e.id)
    return resposta

@api_bp.route('/eventos/<int:evento_id>', methods=['PUT', 'PATCH'])
@login_required
def atualizar(evento_id):
    e = EventoDAO.buscar(evento_id)
    if not e:
        return jsonify({'erro':'Evento nao encontrado.'}), 404
    if not request.is_json:
        return jsonify({'erro':'Envie JSON.'}), 415
    try:
        dados = validar_evento(request.get_json(silent=True), parcial=request.method == 'PATCH')
    except ValueError as err:
        return jsonify({'erro':str(err)}), 400
    for campo, valor in dados.items():
        setattr(e, campo, valor)
    db.session.commit()
    return jsonify(e.para_dict())

@api_bp.delete('/eventos/<int:evento_id>')
@login_required
def excluir(evento_id):
    e = EventoDAO.buscar(evento_id)
    if not e:
        return jsonify({'erro':'Evento nao encontrado.'}), 404
    EventoDAO.excluir(e)
    return '', 204

@api_bp.get('/feriados/<int:ano>')
def feriados(ano):
    if ano < 2000 or ano > 2100:
        return jsonify({'erro':'Ano invalido.'}), 400
    try:
        with urlopen('https://brasilapi.com.br/api/feriados/v1/' + str(ano), timeout=5) as resposta:
            dados = json.load(resposta)
        if not isinstance(dados, list):
            raise ValueError('Resposta inesperada')
        return jsonify(dados)
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return jsonify({'erro':'API externa indisponivel.'}), 502
