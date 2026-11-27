from extensions import db
class Evento(db.Model):
    __tablename__ = 'evento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    local = db.Column(db.String(120))
    vagas = db.Column(db.Integer, default=0)
    inscricoes = db.relationship('Inscricao', back_populates='evento', cascade='all, delete-orphan')
    def para_dict(self):
        return {'id':self.id,'nome':self.nome,'data':self.data,'local':self.local,'vagas':self.vagas or 0}
