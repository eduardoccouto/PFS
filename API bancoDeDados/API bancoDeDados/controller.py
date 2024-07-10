import psycopg2 as _connector
from dotenv import load_dotenv
import os
from limparTela import *

load_dotenv()

class PostGreeDB:

    def __init__(self):
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_NAME")
        self._host = os.getenv("DB_HOST")
        self._conn = self._getConnection()
        print(self.statusServer())
        limparTela()

    def statusServer(self):
        if self._getConnection is not None:
            return '\nIniciando aplicação...' 
        
    def _getConnection(self):
        return _connector.connect(
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
                    tipo varchar(100) NOT NULL,
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

    def _createTableUsuarios(self):
        try:
            cursor = self._conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS usuarios (
                cpf char(11) PRIMARY KEY,
                nome_usuario varchar(80) NOT NULL UNIQUE,
                senha_usuario varchar(30) NOT NULL,
                numero_telefone_usuario char(11) NOT NULL
            )
            '''
            
            cursor.execute(create_table_query)
            self._conn.commit()
            print("Tabela criada com sucesso!")
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')

    def _createTableComentarios(self):
        try:
            cursor = self._conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS comentarios (
                id_comentario SERIAL PRIMARY KEY,
                cpf_coment char(11) NOT NULL,
                nome_usuario_coment VARCHAR(80) NOT NULL,
                cnpj_coment char(14) NOT NULL,
                nome_prestador_coment VARCHAR(80) NOT NULL,
                data_horario TIMESTAMPTZ NOT NULL,
                tipo varchar(600) NOT NULL,

                FOREIGN KEY (cpf_coment)
                    REFERENCES usuarios(cpf),

                
                FOREIGN KEY (cnpj_coment)
                    REFERENCES prestadores(cnpj)
  
            )
            '''
            
            cursor.execute(create_table_query)
            self._conn.commit()
            print("Tabela criada com sucesso!")
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')

    def _createTableSolicitacoes(self):
        try:
            cursor = self._conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS tipo (
                id_solicitacao SERIAL PRIMARY KEY,
                FOREIGN KEY (cpf_coment)
                    REFERENCES usuarios(cpf),
                FOREIGN KEY (nome_usuario_coment)
                    REFERENCES usuarios(nome_usuario),
                FOREIGN KEY (cnpj_coment)
                    REFERENCES prestadores(cnpj),
                FOREIGN KEY (nome_prestador_coment)
                    REFERENCES prestadores(nome_prestador),
                data_horario TIMESTAMPTZ NOT NULL,
                FOREIGN KEY (id_tipo)
                    REFERENCES tipo(id_tipo),
                FOREIGN KEY (tipo)
                    REFERENCES tipo(tipo),
                status varchar(50) NOT NULL
            )
            '''
            
            cursor.execute(create_table_query)
            self._conn.commit()
            print("Tabela criada com sucesso!")
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')    

    def criar_todas_as_tabelas(self):
        self._createTableEnderecos()
        self._createTableTipo()
        self._createTablePrestadores()
        self._createTableUsuarios()
        self._createTableComentarios()
        self._createTableSolicitacoes()

    # ver qual desses vamos manter
    def get_database_tables(self):
        dict_of_tables = self._querying('SHOW tables;')
        print(f'Lista de tabelas no banco de dados {self._database}!\n')
        for table in dict_of_tables:
            print(' '.join(['-', table['Tables_in_' + self._database]]))
        return dict_of_tables

    def get_database_tables(self):
        dict_of_tables = self._querying(
            """ SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'; """)
        print(f'List of tables on {self._database} database!\n')
        for table in dict_of_tables:
            print(f'- {table[0]}')  # Access the first element of the tuple
        return dict_of_tables
    
    def mostrar_tipos(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM tipo;")

        # Obtenha todos os resultados da consulta
        rows = cursor.fetchall()

        # Formate e imprima os resultados
        for row in rows:
            print(f"[{row[0]}] {row[1]}")

        cursor.close()
    
    def retornaTipo(self, id_tipo):
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT tipo FROM tipo WHERE id_tipo = {id_tipo};")

        # Obtenha todos os resultados da consulta
        result = cursor.fetchall()
        for tupla in result:
            result = (tupla[0])
        cursor.close()
        if result:
            return result
        return False
        
            
    def desc_table(self, table):
        return self._querying(' '.join(['DESC', table]))

    def get_lines_from_table(self, table, limit=False, number_of_lines=10):
        query = ' '.join(['SELECT * FROM', table])
        query = query if limit is False else ' '.join([query, 'limit', str(number_of_lines)])

        result = self._querying(query)
        for element in result:
            keys = element.keys()
            for k in keys:
                print(k+':', element[k])
            print('\n')

        return result

    def get_database_name(self):
        return self._database

    # método para adicionar algo, por exempl, então precisa do dicionáio
    def _execute_query_with_dict(self, query: str, attr: dict):
        try:
            cursor = self._conn.cursor()
            cursor.execute(query, attr)
            self._conn.commit()
        except TypeError as err:
            raise (f'An error occur during the insert ' +
                    f'operation on {self._database}\n Message:'
                    f'{err}')
        
    
        
    # método para quando não é necessario receber um dicionário de informações
    def _querying(self, query: str):

        if (not self._getConnection()) or self._conn is None:
            self._conn = self._getConnection()

        cursor = self._conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall() # recupera todos os resultados restantes de uma consulta executada anteriormente
        cursor.close()

        return result
    
    # acredito que isso seja tipo um toString ner
    def _retornar_lista_de_chaves_e_placeholders(self, attr: dict):
        lista_de_chaves = ', '.join([chave for chave in attr.keys()])
        marcadores = ', '.join([f'%({chave})s' for chave in attr.keys()])
        return lista_de_chaves, marcadores

    # verifica se a tabela está no banco de dados
    def _is_on_database(self, table_name:str) -> None:
        if table_name not in self._get_list_of_database_tables():
            raise f'Table not found in the {self._database} database'

    

    def _get_list_of_database_tables(self):
        dict_of_tables = self._querying('SHOW tables;')
        return [table['Tables_in_' + self._database] for table in dict_of_tables]


    

    #CRUD operations
    def create_line(self, attr: dict, table_name: str):
        key_list, placeholders = self._retornar_lista_de_chaves_e_placeholders(attr)
        insertion_query = f"INSERT INTO {table_name} ({key_list}) VALUES ({placeholders})"
        
        try:
            self._execute_query_with_dict(insertion_query, attr)
        except Exception as err:
            raise Exception(f'Message: {err}')  # Levanta uma instância de Exception com a mensagem do erro

        self._conn.commit()
        return True



    def read_table(self, table_name):
        self._is_on_database(table_name)
        return self.get_lines_from_table(table=table_name)


    def update_users_by_id(self, id, data: dict):
        '''''
            Vamos receber um conjunto prédefinido de campos a serem atualizados
        :param id:
        :param data:
        :return:
        '''
        data["id"] = id
        update_query = "UPDATE users SET name = %(name)s"
        self._execute_query_with_dict(update_query, data)
        self._conn.commit()

    def delete_instance(self, table_name: str, condition: str, value):
        self._is_on_database(table_name)
        delete_query = f"DELETE FROM {table_name} WHERE {condition} = %s"
        self._execute_query_with_dict(delete_query, value)
        self._conn.commit()

    def buscar_endereco_por_cep(self, cep):
        query = f"SELECT * FROM enderecos WHERE cep = '{cep}'"
        result = self._querying(query)
        if result:
            return result  # Retorna o primeiro (e único) resultado
        return None
    
    def _buscar_cnpj(self, cnpj):
        query = f"SELECT * FROM prestadores WHERE cnpj = '{cnpj}'"
        result = self._querying(query)
        if result:
            return False  
        return True
    
    def validar_login_prestador(self, cnpj, senha):
        query = f""" SELECT * FROM prestadores WHERE cnpj = '{cnpj}' AND senha_prestador = '{senha}'; """
        result = self._querying(query)
        if result:
            return True 
        return False
    
    def buscar_cpf(self, cpf):
        query = f"SELECT * FROM usuarios WHERE cpf = '{cpf}';"
        if self._querying(query):
            return False
        return True
    
    def validar_login_usuario(self, cpf, senha):
        query = f""" SELECT * FROM usuarios WHERE cpf = '{cpf}' AND senha_usuario = '{senha}'; """
        result = self._querying(query)
        if result:
            return True  # Retorna o primeiro (e único) resultado
        return False
    


        

    


