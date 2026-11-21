import unittest
from app import create_app
from extensions import db
from models.evento import Evento
from models.usuario import Usuario
from models.participante import Participante
from models.inscricao import Inscricao

class TesteSistema(unittest.TestCase):
    def setUp(self):
        self.app=create_app({'TESTING':True,'SECRET_KEY':'chave-de-teste','SQLALCHEMY_DATABASE_URI':'sqlite://'})
        self.ctx=self.app.app_context();self.ctx.push();db.create_all()
        self.client=self.app.test_client();self.client.get('/')
    def tearDown(self):
        db.session.remove();db.drop_all();self.ctx.pop()
    def token(self):
        with self.client.session_transaction() as s:return s['_csrf_token']
    def post(self,url,data):
        return self.client.post(url,data={**data,'csrf_token':self.token()},follow_redirects=True)
    def entrar(self):
        self.post('/cadastro',{'nome':'Gabriel','email':'gabriel@teste.com','senha':'senha-forte-123'})
        return self.post('/login',{'email':'gabriel@teste.com','senha':'senha-forte-123'})
    def test_auth_e_hash(self):
        r=self.entrar();self.assertEqual(r.status_code,200)
        u=Usuario.query.first();self.assertTrue(u.verificar_senha('senha-forte-123'))
        self.assertNotIn('senha-forte-123',u.senha_hash)
    def test_persistencia(self):
        self.entrar();self.post('/eventos',{'nome':'Evento','data':'2026-12-01','local':'Sala','vagas':'3'})
        self.assertEqual(Evento.query.count(),1)
        self.assertEqual(self.client.get('/api/eventos').json[0]['nome'],'Evento')
    def test_api_sem_login(self):
        r=self.client.post('/api/eventos',json={'nome':'X','data':'2026-12-01'},headers={'X-CSRF-Token':self.token()})
        self.assertEqual(r.status_code,401)
    def test_crud_api(self):
        self.entrar();headers={'X-CSRF-Token':self.token()}
        r=self.client.post('/api/eventos',json={'nome':'Teste','data':'2026-12-01','vagas':3},headers=headers)
        self.assertEqual(r.status_code,201);id=r.json['id']
        self.assertEqual(self.client.get('/api/eventos/'+str(id)).status_code,200)
        r=self.client.patch('/api/eventos/'+str(id),json={'nome':'Atualizado'},headers=headers)
        self.assertEqual(r.json['nome'],'Atualizado')
        self.assertEqual(self.client.delete('/api/eventos/'+str(id),headers=headers).status_code,204)
        self.assertEqual(self.client.get('/api/eventos/'+str(id)).status_code,404)
    def test_dados_invalidos(self):
        self.entrar()
        r=self.client.post('/api/eventos',json={'nome':'Teste','data':'nao-e-data'},headers={'X-CSRF-Token':self.token()})
        self.assertEqual(r.status_code,400)
    def test_inscricao_sem_repeticao_sem_exceder_vagas(self):
        e=Evento(nome='Teste',data='2026-12-01',vagas=1);db.session.add(e);db.session.commit()
        url='/eventos/'+str(e.id)+'/inscrever'
        self.post(url,{'nome':'Ana','email':'ana@teste.com'})
        self.post(url,{'nome':'Ana','email':'ana@teste.com'})
        self.post(url,{'nome':'Bia','email':'bia@teste.com'})
        self.assertEqual(Inscricao.query.count(),1)
        self.assertEqual(Participante.query.count(),1)
    def test_csrf(self):
        self.assertEqual(self.client.post('/cadastro',data={'nome':'X'}).status_code,400)
    def test_feriados_ano_invalido(self):
        self.assertEqual(self.client.get('/api/feriados/1900').status_code,400)
if __name__=='__main__':unittest.main()
