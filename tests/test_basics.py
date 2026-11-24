import unittest
from flask import current_app
from app import create_app, db
from app.models import Professor, Disciplina


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_home_mostra_nome_e_prontuario(self):
        html = self.client.get('/').get_data(as_text=True)
        self.assertIn(self.app.config['ALUNO_NOME'], html)
        self.assertIn(self.app.config['ALUNO_PRONTUARIO'], html)

    def test_modulos_nao_desenvolvidos_mostram_nao_disponivel(self):
        for rota in ('/disciplinas', '/alunos', '/cursos', '/ocorrencias'):
            r = self.client.get(rota)
            self.assertEqual(r.status_code, 404)
            self.assertIn('Não disponível', r.get_data(as_text=True))

    def test_so_existem_as_rotas_pedidas(self):
        rotas = {r.rule for r in self.app.url_map.iter_rules()
                 if not r.rule.startswith('/static')}
        self.assertEqual(rotas, {'/', '/professores'})

    def test_select_lista_as_disciplinas(self):
        html = self.client.get('/professores').get_data(as_text=True)
        for codigo in Disciplina.CODIGOS:
            self.assertIn(codigo, html)

    def test_cadastro_persiste_e_lista_professor(self):
        self.client.get('/professores')  # cria as disciplinas
        disc = Disciplina.query.filter_by(codigo='SODA5').first()
        r = self.client.post('/professores', data={'nome': 'Professor André Rufino',
                                                   'disciplina': disc.id})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Professor.query.count(), 1)
        html = self.client.get('/professores').get_data(as_text=True)
        self.assertIn('Professor André Rufino', html)
        self.assertIn('SODA5', html)

    def test_nome_obrigatorio(self):
        self.client.get('/professores')
        disc = Disciplina.query.first()
        self.client.post('/professores', data={'nome': '', 'disciplina': disc.id})
        self.assertEqual(Professor.query.count(), 0)
