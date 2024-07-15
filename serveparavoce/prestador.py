class PrestadorAutenticado:
    def __init__(self, cnpj, senha_prestador):
        self._cnpj = cnpj
        self._senha_prestador = senha_prestador
    
    @property
    def cnpj(self):
        return self._cnpj
        
    