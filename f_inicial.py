from kivymd.uix.screen import MDScreen
from f_login import Login
from f_cadastro import Cadastro


class Inicial(MDScreen):
    def __init__(self, **kwargs):
        super(Inicial, self).__init__(**kwargs)
        self.alerta_msg = None

    def logar(self):
        self.manager.current = 'tela_login'

    def cadastro(self):
        self.manager.current = 'tela_cadastro'
