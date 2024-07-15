from limparTela import limparTela # Importa a função limparTela do módulo limparTela
import os # Importa o módulo os para interagir com variáveis de ambiente
import psycopg2 as _connector # Importa o módulo psycopg2 para conectar ao banco de dados PostgreSQL
from dotenv import load_dotenv # Importa a função load_dotenv do módulo dotenv para carregar variáveis de ambiente de um arquivo .env

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env para o ambiente do sistema

# Define a classe CreateConnection
class CreateConnection:

    # Método inicializador da classe
    def __init__(self):
        
        self._user = os.getenv("DB_USER") # Obtém o valor da variável de ambiente DB_USER e armazena em self._user
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_NAME")
        self._host = os.getenv("DB_HOST")
        self._conn = self.getConnection()
        # Imprime o status do servidor chamando o método statusServer
        print(self.statusServer())
        # Chama a função limparTela para limpar a tela
        limparTela()

    # Método que retorna o status do servidor
    def statusServer(self):
        # Verifica se getConnection não é None
        if self.getConnection is not None:
            # Retorna uma mensagem de status
            return '\nIniciando aplicação...' 
        
    # Método que cria e retorna uma conexão com o banco de dados
    def getConnection(self):
        # Conecta ao banco de dados usando os detalhes fornecidos e retorna o objeto de conexão
        return _connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._database
        )
