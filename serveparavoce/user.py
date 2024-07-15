class UsuarioAutenticado:
    def __init__(self, cpf, senha_usuario):
        self._cpf = cpf
        self._senha_usuario = senha_usuario
        
    @property
    def cpf(self):
        return self._cpf
    
    