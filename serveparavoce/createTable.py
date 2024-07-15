from createConnection import CreateConnection

class CreateTables(CreateConnection):
    def __init__(self):
        super().__init__()
    
    
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
    
    def _createTableAvaliacoesPrestadores(self):
        try:
            cursor = self._conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS avaliacoes_prestadores (
                id_avaliacao_prestador SERIAL PRIMARY KEY,
                cnpj_av char(14) NOT NULL,
                nome_prestador_av VARCHAR(80) NOT NULL,
                cpf_av char(11) NOT NULL,
                nome_cliente_av VARCHAR(80) NOT NULL,
                descricao varchar(600) NOT NULL,

                FOREIGN KEY (cnpj_av)
                    REFERENCES prestadores(cnpj),
                
                FOREIGN KEY (cpf_av)
                    REFERENCES usuarios(cpf)
            )
            '''
            
            cursor.execute(create_table_query)
            self._conn.commit()
            print("Tabela criada com sucesso!")
        except TypeError as err:
            print(f'Não foi possivel criar a tabela. \nMessage: {err}')
            
    def _createTableAvaliacoesClientes(self):
        try:
            cursor = self._conn.cursor()
            
            # SQL para criar a tabela
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS avaliacoes_clientes (
                id_avaliacao_cliente SERIAL PRIMARY KEY,
                cpf_av char(11) NOT NULL,
                nome_cliente_av VARCHAR(80) NOT NULL,
                cnpj_av char(14) NOT NULL,
                nome_prestador_av VARCHAR(80) NOT NULL, 
                descricao varchar(600) NOT NULL,

                FOREIGN KEY (cpf_av)
                    REFERENCES usuarios(cpf),
                    
                FOREIGN KEY (cnpj_av)
                    REFERENCES prestadores(cnpj)
  
            )
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
        self._createTableAvaliacoesPrestadores()
        self._createTableAvaliacoesClientes()
