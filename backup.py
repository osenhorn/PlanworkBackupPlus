import base64
import pyodbc
import shutil
from dados_locais import DadosLocais
from datetime import datetime, date
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton


class BancoDeDados:
    def __init__(self):
        self.db = DadosLocais()
        self.dados = self.db.verifica_dados()
        self.servidor = self.dados['servidor']
        self.usuario = self.dados['usuario']
        self.senha = self.dados['senha'].encode('utf-8')
        self.senha = str(base64.b64decode(self.senha))
        self.senha = self.senha[2:len(self.senha) - 1]
        self.caminho = self.dados['diretorio']
        self.cliente = self.dados['cliente']
        self.compactar = int(self.dados['compactar'])
        self.hoje = date.today()
        self.arq_log = f"{self.caminho}\\{self.cliente}_{self.hoje}.log"
        self.info_db = "DRIVER={SQL Server};" + f"SERVER={self.servidor};UID={self.usuario};PWD={self.senha}"
        self.alerta_msg = MDDialog(
            text="",
            buttons=[
                MDFillRoundFlatButton(
                    text="OK",
                    text_color=(1, 1, 1, 1),
                    md_bg_color=(40 / 255.0, 90 / 255.0, 140 / 255.0, 1),
                    on_release=self.fechar)])

    def cria_backup(self):
        self.salva_log("Iniciando o processo de backup")

        try:
            con = pyodbc.connect(self.info_db, autocommit=True)
        except Exception as e:
            erro = f'Ocorreu um erro na conexão com o banco de dados:\n{e}'
            self.salva_log(erro)
            self.alerta(erro)
            return False
        self.salva_log("Conectado ao banco de dados")

        try:
            cur = con.cursor()
            query = f"select name from sysdatabases where name like '{self.dados['prefixo']}%'"
            lista_de_bancos = cur.execute(query)
        except Exception as e:
            erro = f'Ocorreu um erro ao obter a lista dos bancos de dados. Erro:\n{e}'
            self.salva_log(erro)
            self.alerta(erro)
            return False

        itens = []
        for db in lista_de_bancos:
            itens.append(db[0])

        if len(itens) == 0:
            erro = f"Nenhum banco encontrado com o prefixo {self.dados['prefixo']}."
            self.salva_log(erro)
            self.alerta(erro)
            return False

        self.salva_log("Obtida a lista de bancos de dados")

        for item in itens:
            self.salva_log(f"Iniciando backup do banco {item}")
            query = f"backup database {item} to disk= '{self.caminho}\\{self.cliente}_{self.hoje}.bkp'"
            try:
                cur.execute(query)
                cur.fatchall()
                self.salva_log(f"O arquivo {item}.bak foi criado com sucesso")
            except Exception as e:
                erro = f"ERRO AO GERAR O BACKUP DO BANCO DE DADOS {item}. MENSAGEM DE ERRO:\n{e}"
                erro += "\nSeguindo com o processo para os demais bancos..."
                self.salva_log(erro)
                self.alerta(erro)
        if self.compactar == 1:
            self.salva_log("Iniciando o processo de compactação...")
            from compactar import Compacta
            self.dados['hoje'] = self.hoje
            compacta = Compacta(self.dados)
            compacta.run()
        return True

    def salva_log(self, mensagem):
        with open(self.arq_log, 'a') as log:
            if not mensagem == '':
                log.write(f'{datetime.now()}:\n{mensagem}\n\n')

    def alerta(self, mensagem):
        self.alerta_msg.text = mensagem
        self.alerta_msg.open()

    def fechar(self, obj):
        self.alerta_msg.dismiss()


if __name__ == '__main__':
    bkp = BancoDeDados()
    bkp.cria_backup()
