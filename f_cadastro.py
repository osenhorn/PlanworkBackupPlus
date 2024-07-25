from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from f_login import Login
from email_validator import validate_email
from f_complementar import Complementares


class Cadastro(MDScreen):
    def __init__(self, **kwargs):
        super(Cadastro, self).__init__(**kwargs)
        self.alerta_msg = None

    def proximo(self):
        if (self.ids.servidor.text and
                self.ids.usuario.text and
                self.ids.senha.text and
                self.ids.prefixo.text and
                self.ids.cliente.text and
                self.ids.numbackups.text):
            try:
                int(self.ids.numbackups.text)
                self.manager.current = 'tela_complementar'
            except:
                self.alerta('O campo "Nº de backups" precisa ser um número inteiro.\n'
                            'Corrija o campo antes de prosseguir.')
                return
        else:
            self.alerta("Todos os campos são obrigatórios. Preencha os campos vazios.")

    def limpar(self):
        self.ids.servidor.text = ""
        self.ids.usuario.text = ""
        self.ids.senha.text = ""
        self.ids.prefixo.text = ""
        self.ids.cliente.text = ""
        self.ids.numbackups.text = ""
        self.manager.ids.cad2.ids.legenda.text = "Sincronizar com a nuvem?"
        self.manager.ids.cad2.ids.nuvem.text = "Selecione o serviço"
        self.manager.ids.cad2.ids.diretorio.text = ""
        self.manager.ids.cad2.ids.compactar.active = False

    def alerta(self, mensagem):
        self.alerta_msg = MDDialog(
            text=mensagem,
            buttons=[
                MDFillRoundFlatButton(
                    text="OK",
                    text_color=(1, 1, 1, 1),
                    md_bg_color=(0, 167 / 255.0, 1, 1),
                    on_release=self.fechar)])
        self.alerta_msg.open()

    def fechar(self, obj):
        self.alerta_msg.dismiss()
