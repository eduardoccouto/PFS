import psycopg2 as connector
from dotenv import load_dotenv
import os

load_dotenv()


class PostGreeDB:

    def __init__(self):
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASS")
        self._database = os.getenv("DATABASE")
        self._host = os.getenv("DB_HOST")
        self._conn = self._getConnection()

    def _getConnection(self):
        return connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._database
        )

    def _createTableEnderecos(self):
        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS enderecos (
                    cep CHAR (8) PRIMARY KEY,
                    logradouro VARCHAR(255) NOT NULL,
                    bairro VARCHAR(100) NOT NULL,
                    cidade VARCHAR(100) NOT NULL
                    
                );
                """
            )
            self._conn.commit()
            print('Tabela criado com sucesso!')
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')

    def _createTableTipo(self):
        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS tipo (
                    id_tipo SERIAL PRIMARY KEY NOT NULL,
                    tipo varchar(100) NOT NULL
            );
                """
            )
            self._conn.commit()
            print('Tabela criado com sucesso!')
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')

    def _createTablePrestadores(self):
        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS prestadores (

                    cnpj char(14) PRIMARY KEY NOT NULL,
                    id_tipo INTEGER not null,
                    cep CHAR (8),
                    logradouro VARCHAR(255) NOT NULL,
                    bairro VARCHAR(100) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    tipo_prestador VARCHAR(100) not null,
                    nome_prestador varchar(80) NOT NULL,
                    senha_prestador varchar(30) NOT NULL,
                    numero_telefone_prestador char(11) NOT NULL,
                    numero_endereco varchar(20) NOT NULL,
                    complemento varchar(255) NOT NULL,
                    descricao TEXT NOT NULL,
                    
                    FOREIGN KEY (id_tipo) 
                         REFERENCES tipo(id_tipo),

                    FOREIGN KEY (cep)
                        REFERENCES enderecos(cep)
                    );
                """
            )
            self._conn.commit()
            print('Tabela criado com sucesso!')
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')

    def _querying(self, query: str):

        if self._conn is None:
            self._conn = self._getConnection()

        cursor = self._conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def get_database_tables(self):
        dict_of_tables = self._querying(
            """ SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'; """)
        print(f'List of tables on {self._database} database!\n')
        for table in dict_of_tables:
            print(f'- {table[0]}')  # Access the first element of the tuple
        return dict_of_tables

    def _is_on_database(self, table_name: str):
        if table_name not in self.get_database_tables():
            raise f'Table not found int {self._database}'

    def fazer_query_with_dict(self, query: str, attr: dict):
        try:
            cursor = self._conn.cursor()
            cursor.execute(query, attr)
        except connector.Error as err:
            raise (f'Erro durante o processo.'
                   f'Operação em {self._database}\n'
                   f'{err}')

    def _retornar_lista_de_chaves_e_placeholders(self, attr: dict):
        lista_de_chaves = ', '.join([chave for chave in attr.keys()])
        marcadores = ', '.join([f'%({chave})s' for chave in attr.keys()])
        return lista_de_chaves, marcadores

    def _createUser(self, attr: dict, table_name: str):

        lista_de_chaves, marcadores = self._retornar_lista_de_chaves_e_placeholders(attr)
        insertion_query = f"INSERT INTO {table_name} ({lista_de_chaves}) VALUES ({marcadores})"
        try:
            self.fazer_query_with_dict(insertion_query, attr)
        except Exception as err:
            raise f'Message: {err}'
        self._conn.commit()
        return True

