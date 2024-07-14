import pprint
import psycopg2
from controller import *
from user import UsuarioAutenticado
from prestador import PrestadorAutenticado
import time
from limparTela import *
from datetime import datetime
import pytz


if __name__ == "__main__":
    
    try:
        conn = PostGreeDB()
        conn.criar_todas_as_tabelas()
        print('Conexão bem sucedida! \u2665')
        #time.sleep(2)
        limparTela()
        
    except psycopg2.errors as err:
        print('Não foi possivel estabelecer conexão ao banco de dados. '
              f'Erro: {err}')

#retorna valores atribuidos na base de endereços do banco de dados
def buscaCep(cep):
    endereco = conn.buscar_endereco_por_cep(cep=cep)
    marcadores = ('cep', 'logradouro', 'bairro', 'cidade')
    valores = []
    for dados in endereco:
                valores.append(dict(zip(marcadores, dados)))        
    dict_endereco = valores[0]
    
    return dict_endereco # retorna o endereco em um formato de dicionario 
    

def buscarCnpj(cnpj):
    return conn._buscar_cnpj(cnpj=cnpj)

def listaTiposDeServicos():
    return conn.mostrar_tipos()

def cadastraTipo():

    print("====================================")
    listaTiposDeServicos()
    print("====================================")
    op_tipo = input("Informe o cod. do tipo de serviço: ")
    limparTela()
    result = conn.retornaTipo(op_tipo)
    
    return op_tipo, result

# CLIENTE ---------------------------------------------------------------------------------------------------------
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

    while True:
        if (buscarcpf(cpf) is True):
            print("Usuário não cadastrado.")
            break
        else:
            senha = input("Informe sua senha: ")
            if (conn.validar_login_usuario(cpf, senha) == True):
                usuario_autenticado = UsuarioAutenticado(cpf, senha)
                return menu_cliente(usuario_autenticado)
            #executeQuerySelectServices(usuario_autenticado)
            else:
                print("Senha incorreta. ")
                return None

# PRESTADOR -------------------------------------------------------------------------------------------------------
def coletaDadosPrestador(opcaoTipo, resultado, cnpj):
    
    prestador = {}
    prestador['cnpj'] = cnpj
    prestador['id_tipo'] = opcaoTipo   
    prestador['tipo_prestador'] = resultado
    prestador['nome_prestador'] = input("Digite o nome do seu estabelecimento: ")
    prestador['senha_prestador'] = input("Digite sua senha: ")
    prestador['numero_telefone_prestador'] = input("Digite seu número de telefone (apenas números): ")
    prestador['descricao'] = input("Digite a descrição (até 600 caracteres): ")
    
    return prestador
 
def cadastraEndereco(prestador : dict, cep, endereco : dict):
    prestador['cep'] = cep
    prestador['logradouro'] = endereco['logradouro']
    prestador['bairro'] = endereco['bairro']
    prestador['cidade'] = endereco['cidade']
    prestador['numero_endereco'] = input("Digite o número do endereço: ")
    prestador['complemento'] = input("Digite o complemento do endereço: ")
    
    return prestador


def sem_conta_prestador():
    
    cnpj_temp = input("Digite o CNPJ do prestador (14 dígitos): ")

    if (buscarCnpj(cnpj_temp) is False):
        print("CNPJ já está cadastrado.")
        tela_inicial()

    else:
        opcaoTipo, resultado = cadastraTipo()
        
        if (resultado == False):
            print ("Opção inválida.")
        else:
            prestador = coletaDadosPrestador(opcaoTipo=opcaoTipo, resultado= resultado, cnpj=cnpj_temp)
            cep = input("Digite o CEP: ")
            endereco = buscaCep(cep=cep)
            
            if endereco:
                prestador = cadastraEndereco(prestador, cep, endereco)
            else:
                print("CEP não encontrado. Por favor, tente novamente.")

            try:
                conn.create_line(prestador, 'prestadores')
                time.sleep(2)
                limparTela()
                main()
            except psycopg2.errors as e:
                print(f"Erro ao cadastrar prestador: {e}")

            return prestador
    

def login_prestador():
    cnpj = input("Digite seu CNPJ (apenas números): ")

    while True:
        if (conn._buscar_cnpj(cnpj) is True):
            print("Usuário não cadastrado.")
            break
        else:
            senha = input("Informe sua senha: ")
            if (conn.validar_login_prestador(cnpj, senha) == True):
                prestador_autenticado = PrestadorAutenticado(cnpj, senha)
                menu_prestador(prestador_autenticado)
            else:
                print("Senha incorreta. ")
                main()

def modificar_solicitacao(prestador_autenticado):
    print("[1. Agendar serviço]" + "\n[2. Voltar ao menu inicial]")
    op = int(input("Opção: "))

    match op:
        case 1:
            sol = int(input("Digite o ID da solicitação: "))
            status = conn.verificaSolicitacaoPrestador(sol, prestador_autenticado.cnpj)
            if status:
                conn.mudarStatus(sol, "AGENDADO")   
        case 2:
            menu_prestador(prestador_autenticado)

def menu_prestador(prestador_autenticado):
    limparTela()
    print("Seja bem-vindo(a) ao Serve Para Você!")
    
    print("O que você deseja?")
    op = int(input("[1] Visualizar solicitações de serviço" + "\n[2] Meu perfil" +  "\n[3] Sair" + "\nOpção: "))
    cnpj_atual = prestador_autenticado.cnpj
    match op:
        case 1:
            tipo_atual = conn.retornaTipoCNPJ(cnpj_atual)
            conn.visualizar_solicitacoes(tipo_atual)
            modificar_solicitacao(prestador_autenticado)
        case 2:
            print("╔════════════════════════════════╗")
            print("║          Meu Perfil            ║")
            print("╚════════════════════════════════╝")

            print("\n╭────────────────────────────────╮")
            print("│         Informações            │")
            print("╰────────────────────────────────╯")
            conn.retornaPrestador(prestador_autenticado.cnpj) # modificar para nbao aparecer a senha

            print("\n╭────────────────────────────────╮")
            print("│         Solicitações           │")
            print("╰────────────────────────────────╯")
            conn.retornarSolicitacoesPrestador(prestador_autenticado.cnpj)
            print("\nO que você deseja?:")
            op = int(input("[1] Cancelar alguma solicitação" + "\n[2] Voltar ao menu inicial" +  "\n[3] Sair" + "\nOpção: "))
            match op:
                case 1:
                    opSol = int(input("\nQual solicitação você deseja cancelar (ID)? "))
                    if conn.verificaSolicitacao(opSol, prestador_autenticado.cnpj):
                        conn.desmarcarServico(opSol)
                        menu_prestador()
                    else:
                        print("Essa solicitação não existe ou já está realizada.")
                        menu_prestador(prestador_autenticado)
                case 2:
                    limparTela()
                    menu_prestador(prestador_autenticado)

                case 3:
                    limparTela()
                    main()
        case 3:
            limparTela()
            main()
            



def submenuBuscaPrestadores():
    
    print(submenuBuscaServicos())
    opcaoMenuBuscaSerivicos = int(input("Digite: "))
    
    if opcaoMenuBuscaSerivicos == 1:
        marcador_tipo = 'id_tipo'
        listaTiposDeServicos()
        id_tipo_de_servico = input("Digite o cód. do serviço: ")
        return id_tipo_de_servico, marcador_tipo
    
    elif opcaoMenuBuscaSerivicos == 2:
        marcador_cep = 'cep'
        cep_busca_servico = input("informe o CEP: ")
        return cep_busca_servico, marcador_cep
        
    return None, None

def telaUsuario(usuario_autenticado : UsuarioAutenticado):
    print(f"""
Bem-vindo(a) ao Serve para Você! 
Usuário logado: {usuario_autenticado.cpf}
O que você deseja?

1 | [Fazer solicitação]
2 | [Pesquisar serviços]
3 | [Meu perfil]
4 | [Sair] 
""")
          
    op = int(input("Opção: "))
    return op 

def menu_cliente(usuario_autenticado : UsuarioAutenticado):
    op = telaUsuario(usuario_autenticado)
    match op:
        case 1:
            submenuSolicitacao(usuario_autenticado)

        case 2:
            dictFormat(formataSaidaServicosDisponiveis())

        case 3: 
            print("╔════════════════════════════════╗")
            print("║          Meu Perfil            ║")
            print("╚════════════════════════════════╝")

            print("\n╭────────────────────────────────╮")
            print("│         Informações            │")
            print("╰────────────────────────────────╯")
            conn.retornarUsuario(usuario_autenticado.cpf) # modificar para nbao aparecer a senha

            print("\n╭────────────────────────────────╮")
            print("│         Solicitações           │")
            print("╰────────────────────────────────╯")
            conn.retornarSolicitacoesUsuario(usuario_autenticado.cpf)
            print("\nO que você deseja?:")
            op = int(input("[1] Cancelar alguma solicitação" + "\n[2] Voltar ao menu inicial" +  "\n[3] Sair" + "\nOpção: "))
            match op:
                case 1:
                    opSol = int(input("\nQual solicitação você deseja cancelar (ID)? "))
                    if conn.verificaSolicitacao(opSol, usuario_autenticado.cpf):
                        conn.deleta_instance('solicitacoes', f'id_solicitacao={opSol}')
                        menu_cliente()
                    else:
                        print("Essa solicitação não existe ou já está realizada.")
                        menu_cliente(usuario_autenticado)
                case 2:
                    limparTela()
                    menu_cliente(usuario_autenticado)

                case 3:
                    limparTela()
                    main()
        case 4:
            limparTela()
            main()

def executeQuerySelectServices():
    desmpacotando = submenuBuscaPrestadores()
    referencia, marcador = desmpacotando
    query = f""" select nome_prestador, tipo_prestador, descricao from prestadores where {marcador} = '{referencia}'; """
    result_from_query = conn._querying(query)
    return result_from_query



def formataSaidaServicosDisponiveis():

    servicos = executeQuerySelectServices()
    marcadores = ('Nome do Prestador', 'Tipo de Serviço', 'Descrição do Serviço')
    valores = []
    for dados in servicos:
                valores.append(dict(zip(marcadores, dados)))        
    dict_servicos = valores[0]
    
    return dict_servicos  #MEU ESSE NEGOCIO AQUI RETORNA UM DICIOINARIO VOU ME M#####3

def dictFormat(result_from_dict : dict):
    print('\n')
    for j, k in result_from_dict.items():
        print(f'{j}: {k}')
    print('\n')


def submenuSolicitacao(usuario_autenticado : UsuarioAutenticado):
    solicitacao = {}
    opcaoTipo, resultado = cadastraTipo()

    if (resultado == False):
        print ("Opção inválida.")
    else:
        solicitacao['cpf_sol'] = usuario_autenticado.cpf
        solicitacao['nome_usuario_sol'] = conn.procuraNome(usuario_autenticado.cpf)
        solicitacao['cnpj_sol'] = None
        solicitacao['nome_prestador_sol'] = None
        solicitacao['data_horario'] =  datetime.now(pytz.UTC) 
        solicitacao['id_tipo'] = opcaoTipo
        solicitacao['tipo'] = resultado
        solicitacao['status'] = "EM ABERTO"
        try:
            conn.create_line(solicitacao, 'solicitacoes')
            print("Solicitação cadastrada!")
            menu_cliente(usuario_autenticado)
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar solicitação: {e}")

def submenuBuscaServicos():
    
   return """ 
[1. Pesqusar por tipo de serviço]
[2. Pesquisar por CEP  
"""





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
