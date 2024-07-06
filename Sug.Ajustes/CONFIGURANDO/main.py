from controller import PostGreeDB
import pprint
if __name__ == '__main__':
    
    db = PostGreeDB()

    try:
        db.delete_instance("usuarios", "nome_usuario", "eduardo.couto")
        print('Sucesso!')
    except:
        print("Não Foi KKKKKKKK")

""" 
    user = {
        "cpf":"05568035075",
        "nome_usuario":"eduardo.couto",
        "senha_usuario":"admin123",
        "numero_telefone_usuario":"99999"
    }
    lista, marcadores = db._retornar_lista_de_chaves_e_placeholders(user)

    print(lista, marcadores)

    try:
        db._createUser(user, 'usuarios')
        print('Sucesso!')
    except TypeError as err:
        print(f'Não foi possivel.\nMessage: {err}')

"""