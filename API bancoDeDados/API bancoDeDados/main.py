import psycopg2
from controller import *
import os
from user import UsuarioAutenticado
from prestador import PrestadorAutenticado
import time
from limparTela import *

if __name__ == "__main__":
    try:
        conn = PostGreeDB()
        print('Conexão bem sucedida')
        time.sleep(2)
        limparTela()
        
    except psycopg2.errors as err:
        print('Não foi possivel estabelecer conexão ao banco de dados. '
              f'Erro: {err}')


def sem_conta_prestador():
    prestador = {}
    cnpj_temp = input("Digite o CNPJ do prestador (14 dígitos): ")
    limparTela()

    if (conn._buscar_cnpj(cnpj_temp) is False):
        print("CNPJ já está cadastrado.")

    else:
        prestador['cnpj'] = cnpj_temp
        print("Digite o tipo de serviço: ")
        conn.mostrar_tipos() 
        opcaoTipo = input("Opção: ")
        limparTela()
        resultado = conn.retornaTipo(opcaoTipo)

        if (resultado == False):
            print ("Opção inválida.")
        else:
            prestador['id_tipo'] = opcaoTipo   
            prestador['tipo_prestador'] = resultado
            prestador['nome_prestador'] = input("Digite o nome do seu estabelecimento: ")
            limparTela()
            prestador['senha_prestador'] = input("Digite sua senha: ")
            limparTela()
            prestador['numero_telefone_prestador'] = input("Digite seu número de telefone (apenas números): ")
            limparTela()
            prestador['descricao'] = input("Digite a descrição (até 600 caracteres): ")
            limparTela()

            # Coleta e busca do CEP

            cep = input("Digite o CEP: ")
            endereco = conn.buscar_endereco_por_cep(cep)
            limparTela()
            
            marcadores = ('cep', 'logradouro', 'bairro', 'cidade')
            valores = []
            for dados in endereco:
                valores.append(dict(zip(marcadores, dados)))
                
            data_endereco = valores[0]
            
            if endereco:
                prestador['cep'] = cep
                prestador['logradouro'] = data_endereco['logradouro']
                prestador['bairro'] = data_endereco['bairro']
                prestador['cidade'] = data_endereco['cidade']
                prestador['numero_endereco'] = input("Digite o número do endereço: ")
                prestador['complemento'] = input("Digite o complemento do endereço: ")

            else:
                print("CEP não encontrado. Por favor, tente novamente.")

            try:
                conn.create_line(prestador, 'prestadores')
                print("Prestador cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar prestador: {e}")

            return prestador
        
def buscarcpf(cpf):
    return conn.buscar_cpf(cpf)

def obterDadosCliente(cpf):
    cliente = {}
    cliente['cpf'] = cpf
    cliente['nome_usuario'] = input("Digite seu nome: ")
    cliente['senha_usuario'] = input("Digite sua senha: ")
    cliente['numero_telefone_usuario'] = input("Digite seu número de telefone (apenas números): ")
    return cliente
    

def sem_conta_cliente():
    
    while True:
        cpf_temp = input("Digite seu CPF (11 dígitos): ")
        limparTela()
        if not buscarcpf(cpf_temp):  
            print("CPF já está cadastrado.")
            limparTela()
            break
        else:
            cliente = obterDadosCliente(cpf=cpf_temp)
            try:
                conn.create_line(cliente, 'usuarios')
                print("Cliente cadastrado com sucesso!")
                time.sleep(2)
                limparTela()
                main()
                break
            except psycopg2.errors as e:
                print(f"Erro ao cadastrar cliente: {e}")
                break

    return cliente


def login_cliente():
    cpf = input("Digite seu CPF (apenas números): ")
    limparTela()

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
    limparTela()

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

    subopcao = int(input("[1] Criar conta" + 
                       "\n[2] Já possuo conta" + 
                       "\nOpção: "))

    match subopcao:
        case 1:
            if (opcao == 1):
                limparTela()
                sem_conta_prestador()
            elif (opcao == 2):
                limparTela()
                sem_conta_cliente()
            else:
                limparTela()
                print("Opção inválida.")
        case 2:
            if (opcao == 1):
                limparTela()
                login_prestador()
            elif (opcao == 2):
                limparTela()
                login_cliente()
            else:
                limparTela()
                print("Opção inválida.")


def main():
    
   
        opcao = int(input("Você é prestador ou cliente?" + 
                          "\n[1] Prestador" + 
                          "\n[2] Cliente" + 
                          "\nOpção: "))
        match opcao:
            case 1:
                limparTela()
                tela_inicial(1)

            case 2:
                limparTela()
                tela_inicial(2)


main()
