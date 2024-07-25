from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from dados_locais import DadosLocais
from f_cadastro import Cadastro
import base64


class Manager(MDScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)


class PlanworkBackup(MDApp):
    def build(self):
        self.icon = "icon.ico"
        self.theme_cls.primary_palette = 'Gray'
        return Builder.load_file("main.kv")

    def on_start(self):
        db = DadosLocais()
        dados = db.verifica_dados()
        # self.root.current = 'tela_cadastro'
        if dados:
            self.root.ids.cad1.ids.servidor.text = dados["servidor"]
            self.root.ids.cad1.ids.usuario.text = dados["usuario"]
            pwd = dados["senha"]
            pwd = str(base64.b64decode(pwd))
            pwd = pwd[2:len(pwd) - 1]
            self.root.ids.cad1.ids.senha.text = pwd
            self.root.ids.cad1.ids.prefixo.text = dados["prefixo"]
            self.root.ids.cad1.ids.cliente.text = dados["cliente"]
            self.root.ids.cad1.ids.numbackups.text = str(dados["numbackups"])
            if dados["nuvem"] == "Não sincronizar":
                self.root.ids.cad2.ids.legenda.text = "Não será sincronizado."
            else:
                self.root.ids.cad2.ids.legenda.text = "Você selecionou o serviço:"
            self.root.ids.cad2.ids.nuvem.text = dados["nuvem"]
            self.root.ids.cad2.ids.diretorio.text = dados["diretorio"]
            if dados["compactar"] == 1:
                self.root.ids.cad2.ids.compactar.active = True
            else:
                self.root.ids.cad2.ids.compactar.active = False
            self.root.current = 'tela_principal'
        else:
            self.root.current = 'tela_cadastro'


if __name__ == '__main__':
    pwb = PlanworkBackup()
    pwb.run()
