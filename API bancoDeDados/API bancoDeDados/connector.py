import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLDatabase:
    
    def __init__(self):
        self._host = os.getenv("HOST")
        self._password = os.getenv("PASSWD")
        self._database = os.getenv("DATABSE")
        self._user = os.getenv("USERNAME")
        self.conn = self._connecting()
    
    def _connecting(self):
        conn = psycopg2.connect(
            host = self._host,
            database = self._database,
            user = self._user,
            password = self._password
        )
        return conn
    
    def criar_tabela_enderecos(conn):
        try:
            cursor = conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS enderecos (
                cep CHAR (8) PRIMARY KEY NOT NULL,
                logradouro VARCHAR(255) NOT NULL,
                bairro VARCHAR(100) NOT NULL,
                cidade_estado VARCHAR(100) NOT NULL,
                
            )
            '''
            
            cursor.execute(create_table_query)
            conn.commit()
            print("Tabela criada com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao criar a tabela:", error)

    
    def criar_tabela_tipo(conn):
        try:
            cursor = conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS tipo (
                cep CHAR (8) PRIMARY KEY NOT NULL,
                logradouro VARCHAR(255) NOT NULL,
                bairro VARCHAR(100) NOT NULL,
                cidade_estado VARCHAR(100) NOT NULL,
                
            )
            '''
            
            cursor.execute(create_table_query)
            conn.commit()
            print("Tabela criada com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao criar a tabela:", error)

        
    # getters
    def get_database_tables(self):
        dict_of_tables = self._querying('SHOW tables;')
        print(f'List of tables on {self._database} database!\n')
        for table in dict_of_tables:
            print(' '.join(['-', table['Tables_in_'+self._database]]))
        return dict_of_tables

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

    def closing(self):
        if self.conn.is_connected():
            self.conn.close()

    #support methods
    def _execute_query_with_dict(self, query: str, attr: dict):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params= attr)
        except TypeError as err:
            raise (f'An error occur during the insert '
                   f'operation on {self._database}\n Message:'
                   f'{err}')


    def _returning_key_list_and_placeholders(self, attr:dict):
        keys_list = ', '.join([key for key in attr.keys()])
        placeholder = ', '.join([f'%({key})s' for key in attr.keys()])

        return keys_list, placeholder

    def _is_on_database(self, table_name:str) -> None:
        if table_name not in self._get_list_of_database_tables():
            raise f'Table not found in the {self._database} database'

    def _querying(self, query: str):

        if (not self.conn.is_connected()) or self.conn is None:
            self.conn = self._connecting()

        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def _get_list_of_database_tables(self):
        dict_of_tables = self._querying('SHOW tables;')
        return [table['Tables_in_' + self._database] for table in dict_of_tables]


    """ CRUD operations"""
    def create_line(self, attr: dict, table_name: str):
        self._is_on_database(table_name)
        key_list, placeholders = self._returning_key_list_and_placeholders(attr)
        insertion_query = f"INSERT INTO {table_name} ({key_list}) VALUES ({placeholders})"
        
        try:
            self._execute_query_with_dict(insertion_query, attr)
        except Exception as err:
            raise Exception(f'Message: {err}')  # Levanta uma instância de Exception com a mensagem do erro

        self.conn.commit()
        return True



    def read_table(self, table_name):
        self._is_on_database(table_name)
        return self.get_lines_from_table(table=table_name)


    def update_users_by_id(self, id, data: dict):
        """
            Vamos receber um conjunto prédefinido de campos a serem atualizados
        :param id:
        :param data:
        :return:
        """
        data["id"] = id
        update_query = "UPDATE users SET name = %(name)s"
        self._execute_query_with_dict(update_query, data)
        self.conn.commit()

    def delete_instance(self, table_name: str, condition: str, value):
        self._is_on_database(table_name)
        delete_query = f"DELETE FROM {table_name} WHERE {condition} = %s"
        self._execute_query_with_dict(delete_query, value)
        self.conn.commit()