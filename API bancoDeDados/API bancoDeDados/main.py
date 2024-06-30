'''
import pprint
from connector import MySQLDatabase

if __name__ == '__main__':
    print('runing')
    
    try:
        db = MyS
        print(f"Starting the connection...\nStatus: {db.conn.is_connected()}")
        
    
    except ConnectionError as err:
        raise f"Error during the connection. Message: {err}"
    
    
    
    new_instance = {
                    "id": 129,
                    "name": "estadodois",
                    "abbr": "VR",
                    "created_at":"2024-06-17",
                    "updated_at":"2024-06-17"
                    }
    
db.delete_instance('states', 'id', [88] )

'''
from datetime import datetime
import pytz
import connector 
from user import UsuarioAutenticado

# as tabelas tipo e endereços vao ter dados pré-definidos, vamos colocar aki

def coletar_dados_usuario():
        usuario = {}
        usuario['cpf'] = input("Digite seu CPF (apenas números): ")
        # adicionar aqui validação para ser se este cpf já não está cadastrado
        usuario['nome_usuario'] = input("Digite seu nome: ")
        usuario['senha_usuario'] = input("Digite sua senha: ")
        usuario['numero_telefone_usuario'] = input("Digite seu número de telefone (apenas números): ")
        return usuario

def coletar_dados_usuario():
        usuario = {}
        usuario['cpf'] = input("Digite seu CPF (apenas números): ")
        # adicionar aqui validação para ser se este cpf já não está cadastrado
        usuario['nome_usuario'] = input("Digite seu nome: ")
        usuario['senha_usuario'] = input("Digite sua senha: ")
        usuario['numero_telefone_usuario'] = input("Digite seu número de telefone (apenas números): ")
        return usuario
    
def coletar_dados_prestador(db):
        prestador = {}
        prestador['cnpj'] = input("Digite o CNPJ do prestador (14 dígitos): ")
        prestador['id_tipo_prestador'] = input("Digite o ID do tipo de prestador: ")
        prestador['tipo_servico'] = input("Digite o tipo de serviço: ")
        prestador['nome_prestador'] = input("Digite o nome do prestador: ")
        prestador['senha_prestador'] = input("Digite a senha do prestador: ")
        prestador['numero_telefone_prestador'] = input("Digite o número de telefone do prestador (11 dígitos): ")
        prestador['descricao'] = input("Digite a descrição do prestador (até 600 caracteres): ")

        # Coleta e busca do CEP
        while True:
            cep = input("Digite o CEP: ")
            endereco = connector.buscar_endereco_por_cep(db, cep)
            if endereco:
                prestador['cep'] = cep
                prestador['logradouro'] = endereco['logradouro']
                prestador['bairro'] = endereco['bairro']
                prestador['cidade'] = endereco['cidade']
                print(f"Endereço encontrado: {endereco['logradouro']}, {endereco['bairro']}, {endereco['cidade']}")
                break
            else:
                print("CEP não encontrado. Por favor, tente novamente.")

        prestador['numero_endereco'] = input("Digite o número do endereço: ")
        prestador['complemento'] = input("Digite o complemento do endereço: ")

        return prestador

def coletar_dados_comentario(db, usuario_autenticado):
    comentario = {}

    comentario['cpf_coment'] = usuario_autenticado.cpf
    comentario['nome_usuario_coment'] = usuario_autenticado.nome_usuario

    while True:
        cnpj = input("Digite o CNPJ do prestador que você deseja comentar (14 dígitos): ")
        # fzr validação do cnpj
        '''
        if db.verificar_existencia('prestadores', 'cnpj', cnpj):
            comentario['cnpj_coment'] = cnpj
            break
        else:
            print("CNPJ não encontrado. Por favor, verifique e tente novamente.")
        '''
        # ver se não é melhor digitar apenas o nome e o cnpj fzr uma query!!!!
        nome_prestador = db.buscar_nome_prestador(cnpj)
        if nome_prestador:
            comentario['nome_prestador_coment'] = nome_prestador
        else:
            print("Erro: Nome do prestador não encontrado para o CNPJ fornecido.")
            return None

        comentario['data_horario'] = datetime.now(pytz.utc)

        while True:
            tipo = input("Digite seu comentário (até 600 caracteres): ")
            if len(tipo) <= 600:
                comentario['tipo'] = tipo
                break
            else:
                print("O comentário excede 600 caracteres. Por favor, seja mais breve.")

        return comentario

            
            
