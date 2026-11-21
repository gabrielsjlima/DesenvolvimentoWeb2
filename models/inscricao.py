from datetime import datetime, timezone
from extensions import db
class Inscricao(db.Model):
    __tablename__ = 'inscricao'
    __table_args__ = (db.UniqueConstraint('participante_id', 'evento_id', name='uq_participante_evento'),)
    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(db.Integer, db.ForeignKey('participante.id'), nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    data_inscricao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    participante = db.relationship('Participante', back_populates='inscricoes')
    evento = db.relationship('Evento', back_populates='inscricoes')
