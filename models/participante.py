from extensions import db
class Participante(db.Model):
    __tablename__ = 'participante'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    inscricoes = db.relationship('Inscricao', back_populates='participante', cascade='all, delete-orphan')
