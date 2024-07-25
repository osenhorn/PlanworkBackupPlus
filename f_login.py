import json
import requests
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from f_principal import Principal
from dados_locais import DadosLocais


class Login(MDScreen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.alerta_msg = None
        self.api_key = 'AIzaSyDKiCnNU3kLFo3-fG9qW9XDmdpWBw9Do4k'
        self.url_api = 'https://identitytoolkit.googleapis.com/v1/accounts:'
        self.url_banco = 'https://oxalatata-default-rtdb.firebaseio.com/'
        self.id_do_projeto = 'oxalatata'
        self.db = DadosLocais()
        self.dados = self.db.verifica_dados()

    def on_enter(self, *args):
        if self.dados is not None:
            if self.dados[1] is not None and self.dados[2] is not None:
                self.ids.usuario.text = self.dados[1]
                self.ids.senha.text = self.dados[2]

    def logar(self):
        if self.ids.usuario.text == "" or self.ids.senha.text == "":
            self.alerta("Os campos 'usuário' e 'senha' devem ser preenchidos!")
        else:
            dados = json.dumps({'email': self.ids.usuario.text,
                                'password': self.ids.senha.text,
                                'returnSecureToken': True})
            r = requests.post(f'{self.url_api}signInWithPassword', params={'key': self.api_key}, data=dados)
            if str(r) == '<Response [200]>':
                if len(self.dados[1]) > 0:
                    self.manager.current = 'tela_principal'
                    Window.maximize()
                else:
                    self.alerta_msg = MDDialog(
                        text='Deseja salvar seus dados de Login?',
                        buttons=[
                            MDFillRoundFlatButton(
                                text="Sim",
                                text_color=(1, 1, 1, 1),
                                md_bg_color=(40 / 255.0, 90 / 255.0, 140 / 255.0, 1),
                                on_release=self.iniciar
                            ),
                            MDFillRoundFlatButton(
                                text="Não",
                                text_color=(1, 1, 1, 1),
                                md_bg_color=(40 / 255.0, 90 / 255.0, 140 / 255.0, 1),
                                on_release=self.iniciar
                            )
                        ])
                    self.alerta_msg.open()
            else:
                self.alerta('Usuário ou senha incorretos. Verifique se os dados estão corretos e tente novamente.')

    def esqueci(self):
        if self.ids.usuario.text == '':
            self.alerta('Preencha o campo de e-mail para que a mensagem de recuperação de senha possa ser enviada.')
        else:
            dados = json.dumps({"requestType": "PASSWORD_RESET", "email": usuario})
            r = requests.post(f'{self.url_api}sendOobCode', params={'key': self.api_key}, data=dados)
            if str(r) == '<Response [200]>':
                self.alerta('Se o e-mail preenchido estiver correto, em breve você receberá '
                            'uma mensagem com o link para cadastrar uma nova senha.')
            else:
                self.alerta(f'Ocorreu o seguinte erro ao solicitar a recuperação de senha:\n\n{r.text}')

    def limpar(self):
        self.ids.usuario.text = ""
        self.ids.senha.text = ""

    def iniciar(self, obj):
        if obj.text == "Sim":
            self.db.salva_dados(1, self.ids.usuario.text, self.ids.senha.text)
            self.alerta_msg.dismiss()
            self.manager.current = 'tela_principal'
            Window.maximize()
        else:
            self.db.salva_dados(1)
            self.alerta_msg.dismiss()
            self.manager.current = 'tela_principal'
            Window.maximize()

    def alerta(self, mensagem):
        self.alerta_msg = MDDialog(
            text=mensagem,
            buttons=[
                MDFillRoundFlatButton(
                    text="OK",
                    text_color=(1, 1, 1, 1),
                    md_bg_color=(40/255.0, 90/255.0, 140/255.0, 1),
                    on_release=self.fechar)])
        self.alerta_msg.open()

    def fechar(self, obj):
        self.alerta_msg.dismiss()

    def esqueci(self):
        if self.ids.usuario.text == '':
            self.alerta('Preencha o campo de e-mail para que a mensagem possa ser enviada.')
        else:
            resposta = self.auth.esqueceu_senha(self.ids.usuario.text)
            if resposta[0]:
                self.alerta(resposta[1])
            else:
                self.alerta(f'Informe o erro abaixo ao seu time de suporte:\n\n{resposta[1]}')
