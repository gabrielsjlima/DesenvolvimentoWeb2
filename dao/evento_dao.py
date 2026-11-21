from extensions import db
from models.evento import Evento
class EventoDAO:
    @staticmethod
    def listar():
        return db.session.execute(db.select(Evento).order_by(Evento.data, Evento.id)).scalars().all()
    @staticmethod
    def buscar(id):
        return db.session.get(Evento, id)
    @staticmethod
    def salvar(evento):
        db.session.add(evento)
        db.session.commit()
        return evento
    @staticmethod
    def excluir(evento):
        db.session.delete(evento)
        db.session.commit()
