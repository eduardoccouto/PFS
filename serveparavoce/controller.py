from limparTela import *
import psycopg2
from createTable import CreateTables


class PostGreeDB(CreateTables):   
    def __init__(self):
        super().__init__()
        
    #verifica se o status do serviço é diferente de "realizado" e "agendado" na tabela de solicitações.    
    def validaStatus(self, id_solicitacao):
        cursor = self._conn.cursor()
        try:
            cursor.execute(f""" SELECT status FROM solicitacoes WHERE id_solicitacao = {id_solicitacao}; """)
            resultado = cursor.fetchone()

            if resultado is not None and resultado[0] != "REALIZADA" and  resultado[0] != "AGENDADA":
                return resultado[0]
            else:
                return False
        except psycopg2.Error as e:
            print(f"Erro ao verificar solicitação: {e}")
            return False
        finally:
            cursor.close()

    #verifica se o status do serviço é diferente de "realizado" e "agendado" na tabela de solicitações.   
    def verificaSolicitacaoPrestador(self, id_solicitacao, cnpj):
        cursor = self._conn.cursor()
        try:
            cursor.execute(f""" SELECT status FROM solicitacoes WHERE id_solicitacao = {id_solicitacao} AND cnpj_sol='{cnpj}'; """)
            resultado = cursor.fetchone()

            
            if resultado is not None and resultado[0] != "REALIZADA" and  resultado[0] != "AGENDADA":
                return resultado[0]
            else:
                return False
        except psycopg2.Error as e:
            print(f"Erro ao verificar solicitação: {e}")
            return False
        finally:
            cursor.close()

    #verifica se o status do serviço é diferente de "realizado" e "agendado" na tabela de solicitações, utilizando cpf de quem solicitou. 
    def verificaSolicitacao(self, id_solicitacao, cpf):
        cursor = self._conn.cursor()
        try:
            cursor.execute('''SELECT status FROM solicitacoes WHERE id_solicitacao = %s AND cpf_sol = %s;''', (id_solicitacao, cpf))
            resultado = cursor.fetchone()
            if resultado:  # Verifica se algum resultado foi retornado
                status = resultado[0]  # Acessa o primeiro (e único) elemento da tupla
                if status != "REALIZADA":
                    return status
            return False
        except psycopg2.Error as e:
            print(f"Erro ao verificar a solicitação: {e}")
            return False
        finally:
            cursor.close()
        
    #função para mudar o status de uma solicitação(AGENDADO, REALIZADO, EM ABERTO)
    def mudarStatus(self, id, novoStatus, cnpj, nome_prestador):
        try:
            cursor = self._conn.cursor()
            query = "UPDATE solicitacoes SET status = %s, nome_prestador_sol = %s, cnpj_sol = %s WHERE id_solicitacao = %s"
            cursor.execute(query, (novoStatus, nome_prestador, cnpj, id))
            self._conn.commit()
            print("Status da solicitação atualizado com sucesso!")
        except psycopg2.Error as e:
            print(f"Erro ao atualizar o status da solicitação: {e}")
        finally:
            cursor.close()

    #retorna o nome de um usuario na tabela com base no cpf
    def procuraNome(self, cpf):
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT nome_usuario FROM usuarios WHERE cpf='{cpf}';")
        nome = cursor.fetchall()
        return nome

    #retorna os dados de um prestador com base no cnpj
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

    #retorna dados basicos de um usuario com base no cpf
    def retornarUsuario(self, cpf):
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE cpf = %s;", (cpf,))
            rows = cursor.fetchall()

            for row in rows:
                print(f"CPF: {row[0]}" + f"\nNome: {row[1]}" + f"\nTelefone: {row[3]}")  

        except psycopg2.Error as e:
            print(f"Erro ao retornar informações do usuário: {e}")

        finally:
            cursor.close()

    #retorna as solicitacoes de um prestador 
    def retornarSolicitacoesPrestador(self, cnpj):
        cursor = self._conn.cursor()
        try:
            
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
    
    #retorna as solicitações de servico de um usuario com base 
    def retornarSolicitacoesUsuario(self, cpf):
        cursor = self._conn.cursor()
        try:
           
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

    #retorna apenas o nome de um prestador
    def retornarNome(self, cnpj):
        cursor = self._conn.cursor()
        query = f"""SELECT nome_prestador FROM prestadores WHERE cnpj= '{cnpj}' ;"""
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0]

    #obtém todos os tipos de serviços disponiveis no banco de dados
    def mostrar_tipos(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM tipo;")

        # Obtenha todos os resultados da consulta
        rows = cursor.fetchall()

        # Formate e imprima os resultados
        for row in rows:
            print(f"[{row[0]}] {row[1]}")

        cursor.close()
    
    #Rtorna um tipo de servico com base no id de consulta
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
    
     # Atualiza o status da solicitação para "EM ABERTO" e define o nome do prestador e o CNPJ como None
    def desmarcarServico(self, id_sol):
        cursor = self._conn.cursor()
        try:
           
            cursor.execute('''
                UPDATE solicitacoes
                SET status = 'EM ABERTO', nome_prestador_sol = NULL, cnpj_sol = NULL
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

    #retorna a visualizãção de avaliações do cliente com base na consulta ao bd
    def visualizar_avaliações_clientes(self, cpf):
        cursor = self._conn.cursor()
        try:
            cursor.execute(f"""SELECT * FROM avaliacoes_clientes WHERE cpf_av = '{cpf}'; """)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"\nID da Avaliação: {row[0]}")
                    print(f"CPF do Cliente: {row[1]}")
                    print(f"Nome do Cliente: {row[2]}")
                    print(f"CNPJ do Prestador Avaliador: {row[3]}")
                    print(f"Nome do Prestador Avaliador: {row[4]}")
                    print(f"Avaliação: {row[5]}")
                    print("────────────────────────────────")
            else:
                print("Nenhuma avaliação encontrada para este cliente.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar avaliações do cliente: {e}")

        finally:
            cursor.close()
    
    #retorna a visualizãção de avaliações do prestador com base na consulta ao bd     
    def visualizar_avaliações_prestadores(self, cnpj):
        cursor = self._conn.cursor()
        try:
            cursor.execute(f"""SELECT * FROM avaliacoes_prestadores WHERE cnpj_av = '{cnpj}'; """)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"\nID da Avaliação: {row[0]}")
                    print(f"CNPJ do Prestador: {row[1]}")
                    print(f"Nome do Prestador: {row[2]}")
                    print(f"CPF do Cliente Avaliador: {row[3]}")
                    print(f"Nome do Cliente Avaliador: {row[4]}")
                    print(f"Avaliação: {row[5]}")
                    print("────────────────────────────────")
            else:
                print("Nenhuma avaliação encontrada para este prestador.")

        except psycopg2.Error as e:
            print(f"Erro ao retornar avaliações do prestador: {e}")

        finally:
            cursor.close()

    #deleta uma solicitação da tabela solicitacoes
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
            
    #retorna verdadeira ou falso consforme o resultado da consulta ao bd
    def visualizar_prestador(self, cnpj):
        query = (f"SELECT * FROM prestadores WHERE cnpj='{cnpj}'")
        result = self._querying(query)
        if result:
            return True  
        return False
    
     #retorna verdadeira ou falso consforme o resultado da consulta ao bd
    def visualizar_cliente(self, cpf):
        query = (f"SELECT * FROM usuarios WHERE cnpj='{cpf}'")
        result = self._querying(query)
        if result:
            return True  
        return False

    #retorna falso ou tipo de serviço que o prestador executa com base no bd
    def retornaTipoCNPJ(self, cnpj):
        query = (f"SELECT tipo_prestador FROM prestadores WHERE cnpj='{cnpj}'")
        result = self._querying(query)
        if result:
            return result[0]  
        return False

    #visuliza solicitacoes conforme o tipo
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
    
    #retorna verdadeiro ou falso para o cnpj que realizou solicitações
    def visualizar_servicos_perfil(self, cnpj):
        query = (f"SELECT * FROM solicitacoes WHERE cnpj_sol='{cnpj}'")
        result = self._querying(query)
        if result:
            return True  
        return False
        
    # método para quando não é necessario receber um dicionário de informações
    def _querying(self, query: str):

        if (not self.getConnection()) or self._conn is None:
            self._conn = self.getConnection()

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

    #metodo que recebe o nome da tabela e um dicionario para inserir dados no banco
    def create_line(self, attr: dict, table_name: str):
        key_list, placeholders = self._retornar_lista_de_chaves_e_placeholders(attr)
        insertion_query = f"INSERT INTO {table_name} ({key_list}) VALUES ({placeholders})"
        
        try:
            self._execute_query_with_dict(insertion_query, attr)
        except Exception as err:
            raise Exception(f'Message: {err}')  # Levanta uma instância de Exception com a mensagem do erro

        self._conn.commit()
        return True

    #retorna o resultado de uma busca de endereço pelo cep
    def buscar_endereco_por_cep(self, cep):
        query = f"SELECT * FROM enderecos WHERE cep = '{cep}'"
        result = self._querying(query)
        if result:
            return result  # Retorna o primeiro (e único) resultado
        return None
    
    #retorna o estado da consulta para saber se o prestador está cadastrado na tabela
    def _buscar_cnpj(self, cnpj):
        query = f"SELECT * FROM prestadores WHERE cnpj = '{cnpj}'"
        result = self._querying(query)
        if result:
            return False  
        return True
    
    #retorna verdadeiro ou falso para caso 
    def validar_login_prestador(self, cnpj, senha):
        query = f""" SELECT * FROM prestadores WHERE cnpj = '{cnpj}' AND senha_prestador = '{senha}'; """
        result = self._querying(query)
        if result:
            return True 
        return False
    
    #busca apenas o cpf da tabela
    def buscar_cpf(self, cpf):
        query = f"SELECT * FROM usuarios WHERE cpf = '{cpf}';"
        if self._querying(query):
            return False
        return True
    
    #valida o login do usuario retonando o estado
    def validar_login_usuario(self, cpf, senha):
        query = f""" SELECT * FROM usuarios WHERE cpf = '{cpf}' AND senha_usuario = '{senha}'; """
        result = self._querying(query)
        if result:
            return True  # Retorna o primeiro (e único) resultado
        return False
    


        

    


