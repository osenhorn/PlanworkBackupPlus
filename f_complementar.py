from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.menu import MDDropdownMenu
from dados_locais import DadosLocais
import base64


class Complementares(MDScreen):
    def __init__(self, **kwargs):
        super(Complementares, self).__init__(**kwargs)
        self.alerta_msg = None
        self.db = DadosLocais()
        self.dados = None
        self.update = True
        if self.dados is None:
            self.update = False
        self.selecionado = None
        itens_menu = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in ("Não sincronizar", "OneDrive", "Google Drive")
        ]
        self.menu = MDDropdownMenu(
            items=itens_menu,
            width_mult=4,
        )

    def menu_callback(self, selecionado):
        self.selecionado = selecionado
        self.menu.dismiss()
        self.ids.nuvem.text = selecionado
        if selecionado == "Não sincronizar":
            self.ids.legenda.text = "Não será sincronizado."
        else:
            self.ids.legenda.text = "Você selecionou o serviço:"

    def seleciona_pasta(self):
        from plyer import filechooser
        try:
            self.ids.diretorio.text = filechooser.choose_dir()[0]
        except:
            self.alerta(
                'É necessário selecionar o caminho inteiro do diretório.\nExemplo:\nC:\\Evolution\\Backup',
                False)

    def salvar(self):
        pwd = self.manager.ids.cad1.ids.senha.text
        pwd = pwd.encode('utf-8')
        pwd = str(base64.b64encode(pwd))
        pwd = pwd[2:len(pwd) - 1]
        dados = {
            "servidor": self.manager.ids.cad1.ids.servidor.text,
            "usuario": self.manager.ids.cad1.ids.usuario.text,
            "senha": pwd,
            "prefixo": self.manager.ids.cad1.ids.prefixo.text,
            "cliente": self.manager.ids.cad1.ids.cliente.text,
            "numbackups": self.manager.ids.cad1.ids.numbackups.text,
            "nuvem": self.ids.nuvem.text,
            "diretorio": self.ids.diretorio.text,
            "ultimo": "",
            "compactar": self.ids.compactar.active
        }

        self.db.salva_dados(self.update, dados)

        self.alerta("Dados salvos com sucesso.", True)

    def alerta(self, mensagem, final=False):
        if final:
            self.alerta_msg = MDDialog(
                text=mensagem,
                buttons=[
                    MDFillRoundFlatButton(
                        text="OK",
                        text_color=(1, 1, 1, 1),
                        md_bg_color=(40/255.0, 90/255.0, 140/255.0, 1),
                        on_release=self.fechar_final)])
        else:
            self.alerta_msg = MDDialog(
                text=mensagem,
                buttons=[
                    MDFillRoundFlatButton(
                        text="OK",
                        text_color=(1, 1, 1, 1),
                        md_bg_color=(40 / 255.0, 90 / 255.0, 140 / 255.0, 1),
                        on_release=self.fechar)])
        self.alerta_msg.open()

    def fechar(self, obj):
        self.alerta_msg.dismiss()

    def fechar_final(self, obj):
        self.alerta_msg.dismiss()
        self.manager.current = "tela_principal"
