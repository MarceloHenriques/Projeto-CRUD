from time import sleep

class Vendedor: 
    def __init__(self, nome: str, cpf: str, id_vendedor: int) -> None: # Metodo contrutor da classe
        self._nome = nome
        self._cpf = cpf
        self.id_vendedor = id_vendedor
        
    @property # Getter do atributo nome
    def nome(self) -> str:
        return self._nome

    @nome.setter # Setter do atributo nome
    def nome(self, nome: str) -> None:
        if nome:
            self._nome = nome
        else:
            raise ValueError("O nome não pode ser vazio.")

    @property # Getter do atributo CPF
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter #Setter do atributo CPF com a verificação de digitos numeros e do CPF tem 11 numeros.
    def cpf(self, cpf: str) -> None:
        if cpf.isdigit() and len(cpf) == 11:
            self._cpf = cpf
        else:
            raise ValueError("O CPF deve conter apenas números e ter exatamente 11 dígitos.")
    
    @staticmethod # indica que este método é um método estático ele retorna ler_vendedores
    def ler_vendedores() -> list: # Função para leitura dos dados do vendedor
        vendedores = [] # Inicializando a lista
        try: 
            with open('dados.txt', 'r') as arquivo: # Inicia o arquivo dados.txt
                for linha in arquivo:
                    partes = linha.strip().split('|') # Formata como deve aparecer a linha de dados
                    if len(partes) == 3: # Informa que a linha de dados tem 3 partes
                        id_vendedor = int(partes[0].strip()) # Tranforma a ID do vendedor em INT e adiciona ele na posição 1 da lista
                        nome = partes[1].strip() # Adiciona nome a segunda posição da lista
                        cpf = partes[2].strip() # Adiciona CPF a terceira posição da lista

                        if cpf.isdigit() and len(cpf) == 11: # Verificação se o CPF são somente numeros e tem 11 digitos
                            vendedor = Vendedor(nome, cpf, id_vendedor)
                            vendedores.append(vendedor)
                        else:
                            print(f"Erro no CPF: {cpf} (ID: {id_vendedor}). CPF inválido!")
        except FileNotFoundError:
            pass  # Se o arquivo não existir, retorna uma lista vazia
        return vendedores

    def incluir_vendedor(self) -> None: # Fnção para inclusão de vendedores
        vendedores = Vendedor.ler_vendedores()# Le a lista de vendedores existente

        if any(vendedor.id_vendedor == self.id_vendedor for vendedor in vendedores): # Verifica se já existe um vendedor com o mesmo ID na lista
            print(f"Erro: Já existe um vendedor com o ID {self.id_vendedor}.") # Exibe uma mensagem de erro se o ID do vendedor já estiver em uso
            return

        if not (self.cpf.isdigit() and len(self.cpf) == 11): # Validação do CPF: verifica se o CPF contém apenas números e tem exatamente 11 dígitos
            print(f"Erro: O CPF deve conter apenas números e ter exatamente 11 dígitos. CPF informado: {self.cpf}") # Exibe uma mensagem de erro se o CPF for inválido
            return

        with open('dados.txt', 'a') as arquivo: # Abre o arquivo 'dados.txt' em modo de adição (append) para registrar o novo vendedor
            linha = f"{self.id_vendedor} | {self.nome} | {self.cpf}\n"# Formata a linha que será adicionada ao arquivo
            arquivo.write(linha) # Escrve a linha no arquivo
        print("Vendedor cadastrado com sucesso!") 

    @staticmethod # indica que este método é um método estático ele retorna ler_vendedores
    def atualizar_vendedor(id_vendedor: int, nome: str, cpf: str) -> None: # Função para atualizar o vendedor
        vendedores = Vendedor.ler_vendedores() # Lê a lista de vendedores existentes a partir do arquivo de dados

        vendedor_encontrado = False # Inicializa uma variável para verificar se o vendedor foi encontrado
        for vendedor in vendedores: # Percorre a lista de vendedores para encontrar o vendedor com o ID especificado
            if vendedor.id_vendedor == id_vendedor: # Verifica se o ID do vendedor corresponde ao fornecido
                vendedor_encontrado = True # Marca que o vendedor foi encontrado
                vendedor.nome = nome if nome else vendedor.nome # Atualiza o nome do vendedor 
                vendedor.cpf = cpf if cpf else vendedor.cpf # Atualiza o CPF do vendedor
                break

        if not vendedor_encontrado: # Se o vendedor não foi encontrado, exibe uma mensagem de erro e encerra a função
            print(f"Erro: O vendedor com ID {id_vendedor} não foi encontrado.")
            return

        with open('dados.txt', 'w') as arquivo: # Se tudo estiver correto, atualiza o vendedor no arquivo
            for vendedor in vendedores:
                linha = f"{vendedor.id_vendedor} | {vendedor.nome} | {vendedor.cpf}\n"
                arquivo.write(linha)
        print("Vendedor atualizado com sucesso!")

    @staticmethod # indica que este método é um método estático ele retorna ler_vendedores
    def deletar_vendedor(id_vendedor: int) -> None: # Função para deletar o registro do vendedor
        vendedores = Vendedor.ler_vendedores() # Lê a lista de vendedores existentes a partir do arquivo de dados

        vendedor_encontrado = False # Inicializa uma variável para verificar se o vendedor foi encontrado
        for vendedor in vendedores: # Percorre a lista de vendedores para encontrar o vendedor com o ID especificado
            if vendedor.id_vendedor == id_vendedor: # Verifica se o ID do vendedor corresponde ao fornecido
                vendedor_encontrado = True # Marca que o vendedor foi encontrado
                break

        if not vendedor_encontrado: # Se o vendedor não foi encontrado, exibe uma mensagem de erro e encerra a função
            print(f"Erro: O vendedor com ID {id_vendedor} não foi encontrado.") 
            return

        with open('dados.txt', 'w') as arquivo: # Se o vendedor foi encontrado, reescreve o arquivo de dados sem incluir o vendedor deletado
            for vendedor in vendedores:
                if vendedor.id_vendedor != id_vendedor:
                    linha = f"{vendedor.id_vendedor} | {vendedor.nome} | {vendedor.cpf}\n"
                    arquivo.write(linha)
        print("Vendedor deletado com sucesso!")


class Menu:
    def __init__(self):   # Dicionário de opções do menu mapeando as opções de entrada para métodos correspondentes

        self.opcoes = {
            "1": self.cadastrar_vendedor,
            "2": self.listar_vendedores,
            "3": self.atualizar_vendedor,
            "4": self.deletar_vendedor,
            "5": self.sair
        }
        self.executar =  True # Controle para manter o menu em execução

    
    def exibir_menu(self): # Exibe as opções do menu para o usuário
        print("\n===== BASE DE DADOS VENDEDORES =====")
        print("""
            1 - Cadastrar Vendedor (Create)
            2 - Listar Vendedores (Read)
            3 - Atualizar Vendedor (Update)
            4 - Deletar Vendedor (Delete)
            5 - Sair
            """)

    def escolher_opcao(self, opcao): # Seleciona a função a ser chamada com base na opção do usuário
        acao = self.opcoes.get(opcao) # Obtém a função associada à opção
        if acao:
            acao() # Executa a função correspondente
        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            
    def iniciar(self): # Mantém o menu rodando até o usuário escolher sair
        while self.executar:
            self.exibir_menu() # Mostra o menu
            opcao = input('Escolha a opção desejada: ') # Coleta a opção
            self.escolher_opcao(opcao) # Processa a opção escolhida

    def cadastrar_vendedor(self):  # Método para cadastrar um novo vendedor
        while True:
            nome = input('Nome do Vendedor: ').upper()
            cpf = input('CPF do vendedor: ')
            id_vendedor = input('ID do vendedor: ')
            try:
                id_vendedor = int(id_vendedor) # Verifica se o ID é numérico
                vendedor = Vendedor(nome, cpf, id_vendedor) # Cria uma instância de Vendedor
                vendedor.incluir_vendedor() # Chama o método para incluir o vendedor
                break # Sai do loop se não houver erros
            except ValueError as e: # Tratamento de erro caso o ID não seja válido
                print(f"Erro no cadastro: {e}")
                print("Por favor, insira os dados corretamente.")
    
    def listar_vendedores(self):  # Método para listar todos os vendedores
        vendedores = Vendedor.ler_vendedores() # Lê os vendedores do arquivo
        if vendedores:
            print("\n===== Lista de Vendedores =====")
            for vendedor in vendedores: # Exibe cada vendedor na lista
                print(f"ID: {vendedor.id_vendedor}, Nome: {vendedor.nome}, CPF: {vendedor.cpf}")
        else:  # Caso não existam vendedores cadastrados
            print("Nenhum vendedor cadastrado.")

    def atualizar_vendedor(self): # Método para atualizar os dados de um vendedor
        id_vendedor = input("ID do vendedor a ser atualizado: ")
        try:
            id_vendedor = int(id_vendedor)
            nome = input("Novo Nome do Vendedor (pressione Enter para manter o atual): ").upper()
            cpf = input("Novo CPF do Vendedor (pressione Enter para manter o atual): ")
            Vendedor.atualizar_vendedor(id_vendedor, nome, cpf) # Atualiza o vendedor com base no ID fornecido
        except ValueError: # Tratamento de erro para ID inválido
            print("Erro: O ID do vendedor deve ser um número inteiro.")

    def deletar_vendedor(self): # Método para deletar um vendedor
        id_vendedor = input("ID do Vendedor a ser deletado: ")
        try:
            id_vendedor = int(id_vendedor) # Converte o ID para inteiro
            Vendedor.deletar_vendedor(id_vendedor) # Chama o método de deletar vendedor
        except ValueError: # Tratamento de erro para ID inválido
            print("Erro: O ID do vendedor deve ser um número inteiro.")

    def sair(self): # Método para encerrar o programa
        print("Saindo do programa...")
        sleep(2)
        print("PROGRAMA FINALIZADO")
        self.executar = False # Interrompe o loop do menu, encerrando o programa


menu = Menu() # Cria uma instância da classe Menu
menu.iniciar() # Inicia o loop de execução do menu
