from app import app
from dao.evento_dao import EventoDAO
from models.participante import Participante
with app.app_context():
    print('EVENTOS')
    for e in EventoDAO.listar(): print(e.para_dict())
    print('PARTICIPANTES')
    for p in Participante.query.all(): print(p.id, p.nome, p.email)
