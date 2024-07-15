import psycopg2
from controller import PostGreeDB
from user import UsuarioAutenticado
from prestador import PrestadorAutenticado
import time
from limparTela import *
from datetime import datetime
import pytz


if __name__ == "__main__":
    
    try: #tenta realizar a conexão com o banco de dados instanciando a classe de conexão
        conn = PostGreeDB()
        conn.criar_todas_as_tabelas() #realiza a contrução do objeto 
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

def cadastraTipo(): #retorna o codigo do tipo de serviço e e o tipo de serviço

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
    return cliente #retorna um dicionario com as informações do cliente 
    

def sem_conta_cliente(): #realiza o cadastro do cliente e retona um dicionario com as informções dele
    
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


def login_cliente(): #faz a autenticação do login
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
def coletaDadosPrestador(opcaoTipo, resultado, cnpj): #retorna um dicionario com as informações do funcionário
    
    prestador = {}
    prestador['cnpj'] = cnpj
    prestador['id_tipo'] = opcaoTipo   
    prestador['tipo_prestador'] = resultado
    prestador['nome_prestador'] = input("Digite o nome do seu estabelecimento: ")
    prestador['senha_prestador'] = input("Digite sua senha: ")
    prestador['numero_telefone_prestador'] = input("Digite seu número de telefone (apenas números): ")
    prestador['descricao'] = input("Digite a descrição (até 600 caracteres): ")
    
    return prestador 
 
def cadastraEndereco(prestador : dict, cep, endereco : dict): #recebe por parametro o dicionario da 
                                                              #função de coleta de dados e cadastra o endereço
    prestador['cep'] = cep
    prestador['logradouro'] = endereco['logradouro']
    prestador['bairro'] = endereco['bairro']
    prestador['cidade'] = endereco['cidade']
    prestador['numero_endereco'] = input("Digite o número do endereço: ")
    prestador['complemento'] = input("Digite o complemento do endereço: ")
    
    return prestador
#TESTE

def sem_conta_prestador(): #realiza o cadastro do prestador
    
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
    


def login_prestador(): #faz a autenticação do login do prestador
    
    cnpj = input("Digite seu CNPJ (apenas números): ")

    if conn._buscar_cnpj(cnpj) is True:
        print("Usuário não cadastrado \n Digite novamente.")
        return login_prestador()

    else:
        senha = input("Informe sua senha: ")
        if conn.validar_login_prestador(cnpj, senha) is True:
            prestador_autenticado = PrestadorAutenticado(cnpj, senha)
            menu_prestador(prestador_autenticado)
            limparTela()
            return menu_prestador(prestador_autenticado)
            
            
        else:
            print("Senha incorreta. ")
            main()

            


def modificar_solicitacao(prestador_autenticado: PrestadorAutenticado):
    # Exibe as opções do menu
    print("[1. Agendar serviço]\n[2. Voltar ao menu inicial]")
    op = int(input("Opção: "))  # Lê a opção escolhida pelo usuário

    match op:
        case 1:
            sol = input("Digite o ID da solicitação: ")  # Lê o ID da solicitação
            status = conn.validaStatus(sol)  # Verifica o status da solicitação
            if status:
                # Se a solicitação estiver válida, atualiza o status para "AGENDADA"
                nome_prestador = conn.retornarNome(prestador_autenticado.cnpj)
                conn.mudarStatus(sol, "AGENDADA", prestador_autenticado.cnpj, nome_prestador)
                print("Serviço agendado com sucesso.")
            else:
                # Caso contrário, exibe uma mensagem de erro
                print("Solicitação não encontrada ou já agendada.")
                menu_prestador(prestador_autenticado)  # Volta ao menu do prestador
        case 2:
            menu_prestador(prestador_autenticado)  # Volta ao menu do prestador


def menu_prestador(prestador_autenticado: PrestadorAutenticado):
    # Exibe uma mensagem de boas-vindas
    print("Seja bem-vindo(a) ao Serve Para Você!")
    
    # Pergunta ao usuário qual opção deseja
    print("O que você deseja?")
    op = int(input("[1] Visualizar solicitações de serviço" + "\n[2] Meu perfil" +  "\n[3] Avaliações" + "\n[4] Sair" + "\nOpção: "))
    cnpj_atual = prestador_autenticado.cnpj
    match op:
        case 1:
            # Obtém o tipo de CNPJ atual
            tipo_atual = conn.retornaTipoCNPJ(cnpj_atual) #
            gameOfThrones = tipo_atual[0] #
            # Visualiza as solicitações com base no tipo de CNPJ
            conn.visualizar_solicitacoes(gameOfThrones) # 
            # Modifica a solicitação
            modificar_solicitacao(prestador_autenticado)   
        case 2:
            # Exibe informações do perfil
            print("╔════════════════════════════════╗")
            print("║          Meu Perfil            ║")
            print("╚════════════════════════════════╝")

            print("\n╭────────────────────────────────╮")
            print("│         Informações            │")
            print("╰────────────────────────────────╯")
            # Obtém informações do prestador
            conn.retornaPrestador(prestador_autenticado.cnpj) 

            print("\n╭────────────────────────────────╮")
            print("│         Solicitações           │")
            print("╰────────────────────────────────╯")
            # Retorna as solicitações do prestador
            conn.retornarSolicitacoesPrestador(prestador_autenticado.cnpj)
            print("\nO que você deseja?:")
            op = int(input("[1] Cancelar alguma solicitação" + "\n[2] Voltar ao menu inicial" +  "\n[3] Sair" + "\nOpção: "))
            match op:
                case 1:
                    # Solicitação para cancelar uma solicitação específica
                    opSol = int(input("\nQual solicitação você deseja cancelar (ID)? "))
                    if conn.verificaSolicitacaoPrestador(opSol, prestador_autenticado.cnpj):
                        # Cancela o serviço
                        conn.desmarcarServico(opSol)
                        menu_prestador(prestador_autenticado)
                    else:
                        print("Essa solicitação não existe ou já está realizada.")
                        menu_prestador(prestador_autenticado)
                case 2:
                    # Limpa a tela e volta ao menu inicial
                    limparTela()
                    menu_prestador(prestador_autenticado)

                case 3:
                    # Limpa a tela e volta à função principal
                    limparTela()
                    main()

        case 3:
            # Avalia o cliente
            avaliar_cliente(prestador_autenticado)
        case 4:
            # Limpa a tela e volta à função principal
            limparTela()
            main()

            

def submenuBuscaPrestadores():
    # Exibe o submenu de busca de serviços
    print(submenuBuscaServicos())
    opcaoMenuBuscaSerivicos = int(input("Digite: "))  # Lê a opção escolhida pelo usuário
    
    if opcaoMenuBuscaSerivicos == 1:
        marcador_tipo = 'id_tipo'  # Define o marcador para o tipo de serviço
        listaTiposDeServicos()  # Chama a função para listar os tipos de serviço
        id_tipo_de_servico = input("Digite o cód. do serviço: ")  # Lê o código do serviço
        return id_tipo_de_servico, marcador_tipo
    
    elif opcaoMenuBuscaSerivicos == 2:
        marcador_cep = 'cep'  # Define o marcador para o CEP
        cep_busca_servico = input("Informe o CEP: ")  # Lê o CEP informado pelo usuário
        return cep_busca_servico, marcador_cep
        
    return None, None  # Retorna None se nenhuma opção válida for escolhida


def telaUsuario(usuario_autenticado : UsuarioAutenticado): #retorna a opção do menu da tela do usuário
    print(f"""
Bem-vindo(a) ao Serve para Você! 
Usuário logado: {usuario_autenticado.cpf}
O que você deseja?

1 | [Fazer solicitação]
2 | [Pesquisar serviços]
3 | [Meu perfil]
4 | [Avaliações]
5 | [Sair] 
""")
          
    op = int(input("Opção: "))
    return op 

def menu_cliente(usuario_autenticado: UsuarioAutenticado):
    op = telaUsuario(usuario_autenticado)  # Obtém a opção do usuário

    # Verifica a opção escolhida
    match op:
        case 1:
            submenuSolicitacao(usuario_autenticado)  # Chama a função para lidar com solicitações

        case 2:
            # Formata e exibe os serviços disponíveis
            dictFormat(formataSaidaServicosDisponiveis())
            menu_cliente(usuario_autenticado)  # Volta ao menu principal

        case 3:
            print("╔════════════════════════════════╗")
            print("║          Meu Perfil            ║")
            print("╚════════════════════════════════╝")

            # Exibe informações do usuário
            print("\n╭────────────────────────────────╮")
            print("│         Informações            │")
            print("╰────────────────────────────────╯")
            conn.retornarUsuario(usuario_autenticado.cpf)

            # Exibe solicitações do usuário
            print("\n╭────────────────────────────────╮")
            print("│         Solicitações           │")
            print("╰────────────────────────────────╯")
            conn.retornarSolicitacoesUsuario(usuario_autenticado.cpf)

            # Pergunta ao usuário o que deseja fazer
            print("\nO que você deseja?:")
            op = int(input("[1] Cancelar alguma solicitação\n[2] Voltar ao menu inicial\n[3] Sair\nOpção: "))
            match op:
                case 1:
                    opSol = int(input("\nQual solicitação você deseja cancelar (ID)? "))
                    if conn.verificaSolicitacao(opSol, usuario_autenticado.cpf):
                        conn.deleta_instance('solicitacoes', f'id_solicitacao={opSol}')
                        menu_cliente()  # Volta ao menu principal
                    else:
                        print("Essa solicitação não existe ou já está realizada.")
                        menu_cliente(usuario_autenticado)  # Volta ao menu principal

                case 2:
                    limparTela()
                    menu_cliente(usuario_autenticado)  # Volta ao menu principal

                case 3:
                    limparTela()
                    main()  # Sai do programa

        case 4:
            avaliar_prestador(usuario_autenticado)  # Avalia um prestador de serviços

        case 5:
            limparTela()
            main()  # Sai do programa


def executeQuerySelectServices(): #retorna as informações da consulta com base nos marcadores
    desmpacotando = submenuBuscaPrestadores()
    referencia, marcador = desmpacotando
    query = f""" select nome_prestador, tipo_prestador, numero_telefone_prestador, descricao from prestadores where {marcador} = '{referencia}'; """
    result_from_query = conn._querying(query)
    return result_from_query 
 
def avaliar_cliente(prestador_autenticado: PrestadorAutenticado):
    # Exibe uma mensagem para o usuário
    print("O que você deseja?")
    avaliacao = {}
    # Solicita ao usuário que escolha entre fazer uma avaliação ou pesquisar avaliações
    op = int(input("[1] Fazer uma avaliação\n[2] Pesquisar avaliações\nOpção: "))
    match op:
        case 1:
            # Solicita o CPF do cliente para quem deseja fazer a avaliação
            cpf = input("Qual o CPF de quem você deseja fazer a avaliação? ")
            if buscarcpf(cpf) is False:
                # Se o CPF não for encontrado, preenche os dados da avaliação
                avaliacao['cpf_av'] = cpf
                avaliacao['nome_cliente_av'] = conn.procuraNome(cpf)
                avaliacao['cnpj_av'] = prestador_autenticado.cnpj
                avaliacao['nome_prestador_av'] = conn.retornarNome(prestador_autenticado.cnpj)
                avaliacao_desc = input("Faça sua avaliação: ")
                avaliacao['descricao'] = avaliacao_desc
                # Cria uma linha de avaliação na tabela 'avaliacoes_clientes'
                conn.create_line(avaliacao, 'avaliacoes_clientes')
                print("Avaliação cadastrada!")
                time.sleep(3)
                # Volta ao menu do prestador
                menu_prestador(prestador_autenticado)
            else:
                print("CPF inválido.")
        case 2:
            # Solicita o CPF do cliente para visualizar as avaliações
            cpf = input("Qual o CPF de quem você deseja visualizar as avaliações? ")
            # Chama a função para visualizar as avaliações do cliente
            conn.visualizar_avaliações_clientes(cpf)
            time.sleep(4)
            # Volta ao menu do prestador
            menu_prestador(prestador_autenticado)


def avaliar_prestador(usuario_autenticado: UsuarioAutenticado):
    # Solicita ao usuário a escolha da ação
    print("O que você deseja?")
    avaliacao = {}
    op = int(input("[1] Fazer uma avaliação\n[2] Pesquisar avaliações\nOpção: "))
    
    # Trata o caso 1: Fazer uma avaliação
    match op:
        case 1:
            cnpj = input("Qual o CNPJ de quem você deseja fazer a avaliação? ")
            if conn._buscar_cnpj(cnpj) is False:
                # Coleta detalhes da avaliação
                avaliacao['cnpj_av'] = cnpj
                avaliacao['nome_prestador_av'] = conn.retornarNome(cnpj)
                avaliacao['cpf_av'] = usuario_autenticado.cpf
                avaliacao['nome_cliente_av'] = conn.procuraNome(usuario_autenticado.cpf)
                avaliacao_desc = input("Faça sua avaliação: ")
                avaliacao['descricao'] = avaliacao_desc
                # Cria entrada de avaliação
                conn.create_line(avaliacao, 'avaliacoes_prestadores')
                print("Avaliação cadastrada!")
                time.sleep(3)
                menu_cliente(usuario_autenticado)
            else:
                print("CNPJ inválido.")
        
        # Trata o caso 2: Visualizar avaliações
        case 2:
            cnpj = input("Qual o CNPJ de quem você deseja visualizar as avaliações? ")
            conn.visualizar_avaliações_prestadores(cnpj)
            time.sleep(4)
            menu_cliente(usuario_autenticado)

                


def formataSaidaServicosDisponiveis(): #trata uma entrada em formato de tupla para que ela retorna um dicionario 

    servicos = executeQuerySelectServices()
    marcadores = ('Nome do Prestador', 'Tipo de Serviço','Contato', 'Descrição do Serviço')
    valores = []
    for dados in servicos:
                valores.append(dict(zip(marcadores, dados)))        
    dict_servicos = valores[0]
    
    return dict_servicos  

def dictFormat(result_from_dict : dict): #Forma a saida de um dicionário no print
    print('\n')
    for j, k in result_from_dict.items():
        print(f'{j}: {k}')
    print('\n')

def submenuSolicitacao(usuario_autenticado: UsuarioAutenticado):
    # Cria um dicionário vazio para armazenar os dados da solicitação
    solicitacao = {}

    # Chama a função cadastraTipo() para obter a opção de tipo e o resultado
    opcaoTipo, resultado = cadastraTipo()

    # Verifica se a opção é inválida
    if resultado == False:
        print("Opção inválida.")
    else:
        # Preenche os campos do dicionário de solicitação
        solicitacao['cpf_sol'] = usuario_autenticado.cpf
        solicitacao['nome_usuario_sol'] = conn.procuraNome(usuario_autenticado.cpf)
        solicitacao['cnpj_sol'] = None
        solicitacao['nome_prestador_sol'] = None
        solicitacao['data_horario'] = datetime.now(pytz.UTC)
        solicitacao['id_tipo'] = opcaoTipo
        solicitacao['tipo'] = resultado
        solicitacao['status'] = "EM ABERTO"

        try:
            # Tenta criar uma linha na tabela 'solicitacoes'
            conn.create_line(solicitacao, 'solicitacoes')
            print("Solicitação cadastrada!")
            menu_cliente(usuario_autenticado)
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar solicitação: {e}")


def submenuBuscaServicos():
    
   return """ 
[1. Pesquisar por tipo de serviço]
[2. Pesquisar por CEP  
""" #retorna um submenu de serviços



#comandos da tela incial
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
