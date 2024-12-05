import pickle

# Função para salvar os dados da biblioteca em um arquivo
def salvar_dados(biblioteca, filename='biblioteca.dat'):
    with open(filename, 'wb') as f:
        pickle.dump(biblioteca, f)

# Função para carregar os dados da biblioteca de um arquivo
def carregar_dados(filename='biblioteca.dat'):
    try:
        with open(filename, 'rb') as f:
            biblioteca = pickle.load(f)
    except FileNotFoundError:
        biblioteca = Biblioteca()
    return biblioteca

# Decorador para verificar autenticação
def requer_autenticacao(func):
    def wrapper(*args, **kwargs):
        usuario = next((arg for arg in args if isinstance(arg, Usuario)), None)
        if usuario and usuario.autenticado:
            return func(*args, **kwargs)
        else:
            print("Usuário não autenticado.")
            return None
    return wrapper

# Classe Biblioteca
class Biblioteca:
    def __init__(self, livro=None, usuario=None):
        self.livro = livro if livro is not None else []
        self.usuario = usuario if usuario is not None else []

    def adicionar_livro(self, livro):
        self.livro.append(livro)

    def remover_livro(self, isbn):
        self.livro = [livro for livro in self.livro if livro.isbn != isbn]

    def buscar(self, query):
        return [livro for livro in self.livro if query.lower() in livro.titulo.lower() or query.lower() in livro.autor.lower()]

    def registrar_usuario(self, usuario):
        self.usuario.append(usuario)

    @requer_autenticacao
    def emprestar_livro(self, isbn, usuario):
        for livro in self.livro:
            if livro.isbn == isbn and livro.disponivel:
                livro.emprestar()
                print(f"Livro '{livro.titulo}' emprestado para {usuario.nome}.")
                return True
        print("Livro não disponível ou não encontrado.")
        return False

    @requer_autenticacao
    def devolver_livro(self, isbn, usuario):
        for livro in self.livro:
            if livro.isbn == isbn:
                livro.devolucao()
                print(f"Livro '{livro.titulo}' devolvido por {usuario.nome}.")
                return True
        print("Livro não encontrado.")
        return False

# Classe Livro
class Livro:
    def __init__(self, titulo, autor, isbn, disponivel=True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = disponivel

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            return True
        return False

    def devolucao(self):
        self.disponivel = True

    def mostrar_informacoes(self):
        print(f"Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponível: {'Sim' if self.disponivel else 'Não'}")

# Classe Usuario
class Usuario:
    def __init__(self, nome, email, senha, autenticado=False):
        self.nome = nome
        self.email = email
        self.__senha = senha
        self.autenticado = autenticado

    def autenticar(self, senha):
        if self.__senha == senha:
            self.autenticado = True
            return True
        return False

    def logout(self):
        self.autenticado = False


def main():
    biblioteca = carregar_dados()
    usuario = None

    while True:
        print("\n--- Sistema de Biblioteca ---")
        print("1. Registrar Usuário")
        print("2. Login")
        print("3. Adicionar Livro")
        print("4. Buscar Livro")
        print("5. Emprestar Livro")
        print("6. Devolver Livro")
        print("7. Mostrar Catálogo")
        print("8. Salvar e Sair")
        print("------------------------------")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("E-mail: ")
            senha = input("Senha: ")
            usuario = Usuario(nome, email, senha)
            biblioteca.registrar_usuario(usuario)
            print("Usuário registrado com sucesso!")

        elif opcao == "2":
            email = input("E-mail: ")
            senha = input("Senha: ")
            usuario = next((u for u in biblioteca.usuario if u.email == email), None)
            if usuario and usuario.autenticar(senha):
                print(f"Bem-vindo, {usuario.nome}!")
            else:
                print("Credenciais inválidas.")

        elif opcao == "3":
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            isbn = input("ISBN: ")
            livro = Livro(titulo, autor, isbn)
            biblioteca.adicionar_livro(livro)
            print("Livro adicionado com sucesso!")

        elif opcao == "4":
            query = input("Digite o título ou autor: ")
            livros = biblioteca.buscar(query)
            if livros:
                print("\nLivros encontrados:")
                for livro in livros:
                    livro.mostrar_informacoes()
            else:
                print("Nenhum livro encontrado.")

        elif opcao == "5":
            if usuario and usuario.autenticado:
                isbn = input("Digite o ISBN do livro: ")
                biblioteca.emprestar_livro(isbn, usuario)
            else:
                print("Você precisa fazer login para realizar essa ação.")

        elif opcao == "6":
            if usuario and usuario.autenticado:
                isbn = input("Digite o ISBN do livro: ")
                biblioteca.devolver_livro(isbn, usuario)
            else:
                print("Você precisa fazer login para realizar essa ação.")

        elif opcao == "7":
            print("\nCatálogo de livros:")
            for livro in biblioteca.livro:
                livro.mostrar_informacoes()

        elif opcao == "8":
            salvar_dados(biblioteca)
            print("Dados salvos. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
