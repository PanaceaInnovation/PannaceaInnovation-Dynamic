import oracledb

# Função para inserir um novo usuário na tabela
def inserir_usuario(email, apelido, senha, cpf, matricula, autoridade):
    try:
        # Conectar ao banco de dados
        connection = oracledb.connect(
            user="rm97857",
            password="060105",
            dsn="oracle.fiap.com.br:1521/orcl"
        )

        # Criar um cursor
        cursor = connection.cursor()

        # Comando SQL para inserir o usuário
        sql_insert = """
        INSERT INTO cadastrop (email, apelido, senha, cpf, matricula, autoridade)
        VALUES (:email, :apelido, :senha, :cpf, :matricula, :autoridade)
        """
        
        # Executar o comando de inserção
        cursor.execute(sql_insert, email=email, apelido=apelido, senha=senha, cpf=cpf, matricula=matricula, autoridade=autoridade)
        
        # Confirmar a transação
        connection.commit()
        
        print("Usuário cadastrado com sucesso.")

    except oracledb.DatabaseError as e:
        print("Ocorreu um erro ao cadastrar o usuário:", e)

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

# Função para capturar informações do usuário para cadastro
def cadastro_usuario():
    print("Bem-vindo ao cadastro de usuários.")
    
    email = input("Digite o seu email: ")
    apelido = input("Digite o seu apelido: ")
    senha = input("Digite a sua senha: ")
    cpf = input("Digite o seu CPF: ")
    matricula = input("Digite a sua matrícula: ")
    autoridade = input("Digite a autoridade (S/N): ")
    
    inserir_usuario(email, apelido, senha, cpf, matricula, autoridade)

# Função para a tela principal após o login, que exibe os dados do usuário
def tela_principal(dados_usuario):
    print("\nBem-vindo à Tela Principal!")
    while True:
        print("\nOpções:")
        print("1. Ver Perfil")
        print("2. Editar Dados")
        print("3. Sair")
        
        escolha = input("Digite a opção desejada: ")
        
        if escolha == '1':
            print("\n=== Seu Perfil ===")
            print(f"Email: {dados_usuario['email']}")
            print(f"Apelido: {dados_usuario['apelido']}")
            print(f"CPF: {dados_usuario['cpf']}")
            print(f"Matrícula: {dados_usuario['matricula']}")
            print(f"Autoridade: {dados_usuario['autoridade']}")
        elif escolha == '2':
            print("Tela de edição de dados... (não implementada)")
            # Aqui você pode adicionar código para editar dados do usuário
        elif escolha == '3':
            print("Saindo da Tela Principal.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Função para verificar o login do usuário e retornar os dados dele
def verificar_login(email, senha):
    try:
        # Conectar ao banco de dados
        connection = oracledb.connect(
            user="rm97857",
            password="060105",
            dsn="oracle.fiap.com.br:1521/orcl"
        )

        # Criar um cursor
        cursor = connection.cursor()

        # Comando SQL para verificar o login e buscar os dados do usuário
        sql_select = """
        SELECT email, apelido, cpf, matricula, autoridade FROM cadastrop
        WHERE email = :email AND senha = :senha
        """
        
        # Executar o comando de seleção
        cursor.execute(sql_select, email=email, senha=senha)
        
        # Obter o resultado
        dados_usuario = cursor.fetchone()
        
        if dados_usuario:
            # Criar um dicionário para armazenar os dados do usuário
            dados_usuario_dict = {
                "email": dados_usuario[0],
                "apelido": dados_usuario[1],
                "cpf": dados_usuario[2],
                "matricula": dados_usuario[3],
                "autoridade": dados_usuario[4]
            }
            print("Login bem-sucedido.")
            tela_principal(dados_usuario_dict)  # Redirecionar para a tela principal com os dados do usuário
        else:
            print("Email ou senha incorretos.")
            
    except oracledb.DatabaseError as e:
        print("Ocorreu um erro ao tentar fazer login:", e)

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

# Função para capturar informações do usuário para login
def login_usuario():
    print("Bem-vindo ao login.")
    
    email = input("Digite o seu email: ")
    senha = input("Digite a sua senha: ")
    
    verificar_login(email, senha)

# Função principal do programa com loop
def main():
    while True:
        print("\nMenu:")
        print("1. Cadastro")
        print("2. Login")
        print("3. Sair")

        escolha = input("Digite a opção desejada: ")
        
        if escolha == '1':
            cadastro_usuario()
        elif escolha == '2':
            login_usuario()
        elif escolha == '3':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()


