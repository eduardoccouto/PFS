import psycopg2
from controller import *
from user import UsuarioAutenticado
from prestador import PrestadorAutenticado

if __name__ == "__main__":
    try:
        conn = PostGreeDB()
        print('Conexão bem sucessidida')
    except psycopg2.errors as err:
        print('Não foi possivel estabelecer conexão ao banco de dados. '
              f'Erro: {err}')


def sem_conta_prestador():
    prestador = {}

    cnpj_temp = input("Digite o CNPJ do prestador (14 dígitos): ")

    if (conn._buscar_cnpj(cnpj_temp) is False):
        print("CNPJ já está cadastrado.")

    else:
        prestador['cnpj'] = cnpj_temp

        prestador['id_tipo_prestador'] = input("Digite o ID do tipo de prestador: ")
        # como vamos fzr aqui? vamos mostrar a lista e pedir para ele digitar o nº?
        # e a partir do número pesquisar o nome e setar?

        prestador['tipo_servico'] = input("Digite o tipo de serviço: ")
        prestador['nome_prestador'] = input("Digite o nome do prestador: ")
        prestador['senha_prestador'] = input("Digite a senha do prestador: ")
        prestador['numero_telefone_prestador'] = input("Digite o número de telefone do prestador (11 dígitos): ")
        prestador['descricao'] = input("Digite a descrição do prestador (até 600 caracteres): ")

    # Coleta e busca do CEP

    cep = input("Digite o CEP: ")
    endereco = conn.buscar_endereco_por_cep(cep)
    if endereco:
        prestador['cep'] = cep
        prestador['logradouro'] = endereco['logradouro']
        prestador['bairro'] = endereco['bairro']
        prestador['cidade'] = endereco['cidade']
        prestador['numero_endereco'] = input("Digite o número do endereço: ")
        prestador['complemento'] = input("Digite o complemento do endereço: ")

    else:
        print("CEP não encontrado. Por favor, tente novamente.")

    query = """ INSERT INTO prestadores (cnpj, id_tipo_prestador, tipo_prestador, nome_prestador, senha_prestador, numero_telefone_prestador, descricao)
                VALUES (%(cnpj)s,%(id_tipo_prestador)s, %(tipo_prestador)s, %(tipo_servico)s, %(nome_prestador)s, 
                        %(senha_prestador)s, %(numero_telefone_prestador)s, %(descricao)s); """
    try:
        conn._execute_query_with_dict(query, prestador)
        print("Prestador cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar prestador: {e}")

    return prestador


def sem_conta_cliente():
    cliente = {}
    while True:
        cpf_temp = input("Digite seu CPF (11 dígitos): ")
        if not conn.buscar_cpf(cpf_temp):  # Supondo que buscar_cpf retorna False se o CPF já está cadastrado
            print("CPF já está cadastrado.")
            break
        else:
            # Adiciona validação para ver se este CPF já não está cadastrado
            cliente['cpf'] = cpf_temp
            cliente['nome_usuario'] = input("Digite seu nome: ")
            cliente['senha_usuario'] = input("Digite sua senha: ")
            cliente['numero_telefone_usuario'] = input("Digite seu número de telefone (apenas números): ")

            # Inserir cliente no banco de dados
            query = """
            INSERT INTO usuarios (cpf, nome_usuario, senha_usuario, numero_telefone_usuario)
            VALUES (%(cpf)s, %(nome_usuario)s, %(senha_usuario)s, %(numero_telefone_usuario)s);
            """
            try:
                conn._execute_query_with_dict(query, cliente)
                print("Cliente cadastrado com sucesso!")
                break
            except psycopg2.errors as e:
                print(f"Erro ao cadastrar cliente: {e}")
                break

    return cliente


def login_cliente():
    cpf = input("Digite seu CPF (apenas números): ")

    while True:
        if (conn.buscar_cpf(cpf) is True):
            print("Usuário não cadastrado.")
            break
        else:
            senha = input("Informe sua senha: ")
            if (conn.validar_login_usuario == True):
                usuario_autenticado = UsuarioAutenticado(cpf, senha)
                return usuario_autenticado
            else:
                print("Senha incorreta. ")
                return None


def login_prestador():
    cnpj = input("Digite seu CNPJ (apenas números)" + '\nDigite :')

    while True:
        if (conn._buscar_cnpj(cnpj) is True):
            print("Usuário não cadastrado.")
            break
        else:
            senha = input("Informe sua senha: ")
            if (conn.validar_login_prestador == True):
                usuario_autenticado = PrestadorAutenticado(cnpj, senha)
                return usuario_autenticado
            else:
                print("Senha incorreta. ")
                return None


def tela_inicial(opcao):

    subopcao = int(input("[1] Criar conta" + "\n[2] Já possuo conta" + "\nOpção: "))

    match subopcao:
        case 1:
            if (opcao == 1):
                sem_conta_prestador()
            elif (opcao == 2):
                sem_conta_cliente()
            else:
                print("Opção inválida.")
        case 2:
            if (opcao == 1):
                login_prestador()
            elif (opcao == 2):
                login_cliente()
            else:
                print("Opção inválida.")


def main():
    opcao = int(input("Você é prestador ou cliente?" + "\n[1] Prestador" + "\n[2] Cliente" + "\n"))
    match opcao:
        case 1:
            tela_inicial(1)

        case 2:
            tela_inicial(2)


main()
