import sqlite3 as lite
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton


class DadosLocais:
    def __init__(self, **kwargs):
        self.alerta_msg = MDDialog(
            text="",
            buttons=[
                MDFillRoundFlatButton(
                    text="OK",
                    text_color=(1, 1, 1, 1),
                    md_bg_color=(40/255.0, 90/255.0, 140/255.0, 1),
                    on_release=self.fechar)])
        self.retorno = None
        self.campos = [
            "servidor",
            "usuario",
            "senha",
            "prefixo",
            "cliente",
            "numbackups",
            "nuvem",
            "diretorio",
            "ultimo",
            "compactar"
        ]
        self.con = None
        try:
            self.con = lite.connect('planworkbackup.db')
        except Exception as e:
            print(e)

        try:
            query = "CREATE TABLE IF NOT EXISTS dados_backup("
            query += "servidor TEXT,usuario TEXT,senha TEXT,prefixo TEXT,cliente TEXT,"
            query += "numbackups NUMERIC,nuvem TEXT,diretorio TEXT,ultimo TEXT,compactar BOOLEAN)"
            self.executar(
                query,
                False)

        except Exception as e:
            self.alerta(f"Ocorreu um erro ao criar o banco de dados local. Mensagem:\n\n{e}")

    def verifica_dados(self):
        if self.retorno is not None:
            return self.retorno
        dados = self.executar("select * from dados_backup", True)
        self.retorno = {}
        if len(dados) > 0:
            for i in range(len(self.campos)):
                self.retorno[self.campos[i]] = dados[0][i]
            return self.retorno
        return None

    def salva_dados(self, update, dados=None):
        campos = "servidor,usuario,senha,prefixo,cliente,numbackups,nuvem,diretorio,ultimo,compactar"
        valores = ''
        query = ''
        if update:
            for i in dados:
                if i != 'numbackups' and i != 'compactar':
                    valores = valores + f"{i} = '{dados[i]}', "
                else:
                    if i == 'numbackups':
                        valores = valores + f"{i} = {dados[i]}, "
                    if i == 'compactar':

                        valores = valores + f"{i} = {dados[i]}"

            query = f"UPDATE dados_backup SET {valores}"
        else:
            for i in dados:
                if i != 'numbackups' and i != 'compactar':
                    valores = valores + f"'{dados[i]}',"
                else:
                    if i == 'numbackups':
                        valores = valores + f"{dados[i]},"
                    if i == 'compactar':
                        valores = valores + f"{dados[i]}"

            query = f"INSERT INTO dados_backup({campos}) VALUES ({valores})"

        self.executar(query, False)

    def executar(self, query, retorno=False):
        with self.con as cur:
            dados = cur.execute(query).fetchall()
        if retorno:
            return dados
        return

    def alerta(self, mensagem):
        self.alerta_msg.text = mensagem
        self.alerta_msg.open()

    def fechar(self, obj):
        self.alerta_msg.dismiss()
