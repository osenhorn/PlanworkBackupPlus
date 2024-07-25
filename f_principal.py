from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDFillRoundFlatButton
from dados_locais import DadosLocais
from backup import BancoDeDados


class Principal(MDScreen):
    def __init__(self, **kwargs):
        super(Principal, self).__init__(**kwargs)
        self.alerta_msg = MDDialog(
            text="",
            buttons=[
                MDFillRoundFlatButton(
                    text="OK",
                    md_bg_color=(0, 167/255.0, 1, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=self.fechar)])
        self.boas_vindas_txt = None

    def novo_backup(self):
        banco = BancoDeDados()
        banco.cria_backup()

    def alerta(self, mensagem):
        self.alerta_msg.text = mensagem
        self.alerta_msg.open()

    def fechar(self):
        self.alerta_msg.dismiss()
