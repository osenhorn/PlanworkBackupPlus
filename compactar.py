import py7zr


class Compacta:
    def __init__(self, dados):
        self.servidor = dados['servidor']
        self.usuario = dados['usuario']
        self.senha = dados['senha']
        self.caminho = self.dados['diretorio']
        self.cliente = self.dados['cliente']
        self.compactar = self.dados['compactar']
        self.hoje = dados['hoje']
        self.arq_log = f"{self.caminho}\\{self.cliente}_{self.hoje}.log"
