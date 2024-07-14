import psycopg2 as _connector
from dotenv import load_dotenv
import os
from limparTela import *
import psycopg2

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

                    cnpj CHAR(14) PRIMARY KEY NOT NULL,
                    id_tipo INTEGER NOT NULL,
                    cep CHAR(8),
                    logradouro VARCHAR(255) NOT NULL,
                    bairro VARCHAR(100) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    tipo_prestador VARCHAR(100) NOT NULL,
                    nome_prestador VARCHAR(80) NOT NULL,
                    senha_prestador VARCHAR(30) NOT NULL,
                    numero_telefone_prestador CHAR(11) NOT NULL,
                    numero_endereco VARCHAR(20) NOT NULL,
                    complemento VARCHAR(255) NOT NULL,
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
            CREATE TABLE IF NOT EXISTS solicitacoes (
                id_solicitacao SERIAL PRIMARY KEY,
            cpf_sol char(11) NOT NULL,
            nome_usuario_sol varchar(80) NOT NULL,
            cnpj_sol char(14),
            nome_prestador_sol varchar(80),
            data_horario TIMESTAMPTZ NOT NULL,
            id_tipo int NOT NULL,
            tipo varchar(100) NOT NULL,
            status varchar(50) NOT NULL,

            FOREIGN KEY (cpf_sol)
                REFERENCES usuarios(cpf),

            FOREIGN KEY (cnpj_sol)
                REFERENCES prestadores(cnpj),

            FOREIGN KEY (id_tipo)
                REFERENCES tipo(id_tipo)

           );
            '''
            
            cursor.execute(create_table_query)
            self._conn.commit()
            print("Tabela criada com sucesso!")
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')    

    def criar_todas_as_tabelas(self):
        self._createTableTipo()
        self._createTableEnderecos()
        
        #self._createTablePrestadores()
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
    
    def verificaSolicitacaoPrestador(self, id_solicitacao):
        cursor = self._conn.cursor()
        try:
            cursor.execute(f""" SELECT status FROM solicitacoes WHERE id_solicitacao = {id_solicitacao}; """)
            resultado = cursor.fetchone()

            
            if resultado is not None and resultado[0] != "REALIZADA":
                return resultado[0]
            else:
                return False
        except psycopg2.Error as e:
            print(f"Erro ao verificar solicitação: {e}")
            return False
        finally:
            cursor.close()

    def verificaSolicitacao(self, id_solicitacao, cpf):
        cursor = self._conn.cursor()
        try:
            cursor.execute('''SELECT * FROM solicitacoes WHERE id_solicitacao = %s AND cpf_sol = %s;''', (id_solicitacao, cpf))
            resultado = cursor.fetchone()

            if resultado and resultado != "REALIZADA":
                return resultado[0]
            else:
                return False
        except psycopg2.Error as e:
            print(f"Erro ao verificar solicitação: {e}")
            return False
        finally:
            cursor.close()

    def mudarStatus(self, id, novoStatus):
        try:
            cursor = self._conn.cursor()
            query = "UPDATE solicitacoes SET status = %s WHERE id_solicitacao = %s"
            cursor.execute(query, (novoStatus, id))
            self._conn.commit()
            print("Status da solicitação atualizado com sucesso!")
        except psycopg2.Error as e:
            print(f"Erro ao atualizar o status da solicitação: {e}")
        finally:
            cursor.close()

    def verificaSolicitacaoPrestador(self, id):
        cursor = self._conn.cursor()
        query = f"""SELECT status FROM solicitacoes WHERE id_solicitacao = {id} """
        cursor.execute(query)
        resultado = cursor.fetchall()  # Adicione os parênteses aqui

        if resultado and resultado[0][0] != "REALIZADA":  # Ajuste a verificação
            return resultado[0][0]
        else:
            return False

    def procuraNome(self, cpf):
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT nome_usuario FROM usuarios WHERE cpf='{cpf}';")
        nome = cursor.fetchall()
        return nome

    def retornaPrestador(self, cnpj):
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM prestadores WHERE cnpj = %s;", (cnpj,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"Nome: {row[7]}")
                    print(f"Tipo de Serviço: {row[6]}")
                    print(f"Número de Telefone: {row[9]}")
                    print(f"CEP: {row[2]}")
                    print(f"Logradouro: {row[3]}")
                    print(f"Bairro: {row[4]}")
                    print(f"Cidade: {row[5]}")
                    print(f"Número do Endereço: {row[10]}")
                    print(f"Complemento: {row[11]}")
                    print(f"Descrição: {row[12]}")
                    print("────────────────────────────────")
            else:
                print("Nenhum prestador encontrado.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar informações do usuário: {e}")

        finally:
            cursor.close()

    def retornarUsuario(self, cpf):
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = %s;", (cpf,))
            rows = cursor.fetchall()

            for row in rows:
                print(f"CPF: {row[0]}" + f"\nNome: {row[1]}" + f"\nTelefone: {row[2]}")  

        except psycopg2.Error as e:
            print(f"Erro ao retornar informações do usuário: {e}")

        finally:
            cursor.close()

    def retornarSolicitacoesPrestador(self, cnpj):
        cursor = self._conn.cursor()
        try:
            # Use parâmetros para evitar SQL injection
            cursor.execute('''SELECT * FROM solicitacoes WHERE cnpj_sol = %s;''', (cnpj,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"\nID: {row[0]}")
                    print(f"CNPJ do Prestador: {row[3]}")
                    print(f"Nome do Prestador: {row[4]}")
                    print(f"Data e Horário: {row[5]}")
                    print(f"Tipo: {row[7]}")
                    print(f"Status: {row[8]}")
                    print("────────────────────────────────")
            else:
                print("Nenhuma solicitação encontrada para este CNPJ.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar solicitações do usuário: {e}")

        finally:
            cursor.close()
    
    def retornarSolicitacoesUsuario(self, cpf):
        cursor = self._conn.cursor()
        try:
            # Use parâmetros para evitar SQL injection
            cursor.execute('''SELECT * FROM solicitacoes WHERE cpf_sol = %s;''', (cpf,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"\nID: {row[0]}")
                    print(f"CNPJ do Prestador: {row[3]}")
                    print(f"Nome do Prestador: {row[4]}")
                    print(f"Data e Horário: {row[5]}")
                    print(f"Tipo: {row[7]}")
                    print(f"Status: {row[8]}")
                    print("────────────────────────────────")
            else:
                print("Nenhuma solicitação encontrada para este CPF.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar solicitações do usuário: {e}")

        finally:
            cursor.close()


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

    def desmarcarServico(self, id_sol):
        cursor = self._conn.cursor()
        try:
            # Atualiza o status da solicitação para "EM ABERTO" e define o nome do prestador e o CNPJ como None
            cursor.execute('''
                UPDATE solicitacoes
                SET status = 'EM ABERTO', nome_prestador = NULL, cnpj = NULL
                WHERE id_solicitacao = %s;
            ''', (id_sol,))
            
            # Confirma a transação
            self._conn.commit()
            print(f"Solicitação {id_sol} desmarcada com sucesso.")
        
        except psycopg2.Error as e:
            # Em caso de erro, reverte a transação
            self._conn.rollback()
            print(f"Erro ao desmarcar solicitação: {e}")
        
        finally:
            cursor.close()

    def deleta_instance(self, table_name, condition):
        try:
            cursor = self._conn.cursor()
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            cursor.execute(delete_query)
            self._conn.commit()
            print("Solicitação cancelada com sucesso!")
        except psycopg2.Error as e:
            print(f"Erro ao cancelar a solicitação: {e}")

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
    
    def visualizar_prestador(self, cnpj):
        query = (f"SELECT * FROM prestadores WHERE cnpj='{cnpj}'")
        result = self._querying(query)
        if result:
            return True  
        return False
    
    def visualizar_cliente(self, cpf):
        query = (f"SELECT * FROM usuarios WHERE cnpj='{cpf}'")
        result = self._querying(query)
        if result:
            return True  
        return False

    def retornaTipoCNPJ(self, cnpj):
        query = (f"SELECT tipo_prestador FROM prestadores WHERE cnpj='{cnpj}'")
        result = self._querying(query)
        if result:
            return result[0]  
        return False


    def visualizar_solicitacoes(self, tipo):
        cursor = self._conn.cursor()
        try:
            # Use parâmetros para evitar SQL injection
            cursor.execute(f"""SELECT * FROM solicitacoes WHERE tipo = '{tipo}'; """)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"\nID: {row[0]}")
                    print(f"CNPJ do Prestador: {row[3]}")
                    print(f"Nome do Prestador: {row[4]}")
                    print(f"Data e Horário: {row[5]}")
                    print(f"Tipo: {row[7]}")
                    print(f"Status: {row[8]}")
                    print("────────────────────────────────")
            else:
                print("Nenhuma solicitação encontrada para este tipo.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar solicitações do usuário: {e}")

        finally:
            cursor.close()
    
    def visualizar_servicos_perfil(self, cnpj):
        query = (f"SELECT * FROM solicitacoes WHERE cnpj_sol='{cnpj}'")
        result = self._querying(query)
        if result:
            return True  
        return False
        
    
        
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
    


        

    


