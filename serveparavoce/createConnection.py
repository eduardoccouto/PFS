from limparTela import limparTela
import os
import psycopg2 as _connector
from dotenv import load_dotenv
load_dotenv()

class CreateConnection:

    def __init__(self):
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_NAME")
        self._host = os.getenv("DB_HOST")
        self._conn = self.getConnection()
        print(self.statusServer())
        limparTela()

    def statusServer(self):
        if self.getConnection is not None:
            return '\nIniciando aplicação...' 
        
    def getConnection(self):
        return _connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._database
        )


    
    
        