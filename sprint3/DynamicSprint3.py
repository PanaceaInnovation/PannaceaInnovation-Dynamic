import oracledb # Importando para tornar possível a conexão com a Oracle
import random  # Importando para gerar o número aleatório que será atribuído a pontuação
import pandas as pd # Importando para poder exibir o DataFrame que contém os alunos

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

        # Se o usuário não for professor, gerar uma pontuação aleatória entre 0 e 10, apenas para fins de simulação
        if autoridade == 0:
            pontuacao = random.randint(0, 10)
        else:
            pontuacao = None  # Professores não têm pontuação

        # Comando SQL para inserir o usuário
        sql_insert = """
        INSERT INTO cadastrop (email, apelido, senha, cpf, matricula, autoridade, pontuacao)
        VALUES (:email, :apelido, :senha, :cpf, :matricula, :autoridade, :pontuacao)
        """
        
        # Executar o comando de inserção
        cursor.execute(sql_insert, email=email, apelido=apelido, senha=senha, cpf=cpf, matricula=matricula, autoridade=autoridade, pontuacao=pontuacao)
        
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
    autoridade = int(input("Digite se é uma autoridade (Professor) (1 para sim e 0 para não): "))
    
    inserir_usuario(email, apelido, senha, cpf, matricula, autoridade)

   
# Função para possibilitar a edição de dados do usuário
def editar_dados_usuario(dados_usuario):
    print("\n=== Editar Dados ===")
    
    # Opções para edição
    while True:
        print("\nDados atuais:")
        for key, value in dados_usuario.items():
            print(f"{key.capitalize()}: {value}")
        
        print("\nEscolha o que deseja editar:")
        print("1. Email")
        print("2. Apelido")
        print("3. CPF")
        print("4. Sair")

        escolha = input("Digite a opção desejada: ")

        if escolha == '1':
            novo_email = input("Digite o novo email: ")
            dados_usuario['email'] = novo_email
            
        elif escolha == '2':
            novo_apelido = input("Digite o novo apelido: ")
            dados_usuario['apelido'] = novo_apelido
            
            
        elif escolha == '3':
            novo_cpf = input("Digite o novo CPF: ")
            dados_usuario['cpf'] = novo_cpf
            
        elif escolha == '4':
            break
            
        else:
            print("Opção inválida. Tente novamente.")

        # Após cada edição, perguntar se deseja confirmar as alterações
        confirmar = input("Deseja confirmar as alterações? (s/n): ")
        if confirmar.lower() == 's':
            try:
                # Conectar ao banco de dados
                connection = oracledb.connect(
                    user="rm97857",
                    password="060105",
                    dsn="oracle.fiap.com.br:1521/orcl"
                )

                # Criar um cursor
                cursor = connection.cursor()

                # Comando SQL para atualizar os dados do usuário
                sql_update = """
                UPDATE cadastrop
                SET email = :email, apelido = :apelido, cpf = :cpf
                WHERE matricula = :matricula
                """

                # Executar a atualização
                cursor.execute(sql_update, email=dados_usuario['email'],
                               apelido=dados_usuario['apelido'],
                               cpf=dados_usuario['cpf'],
                               matricula=dados_usuario['matricula'])

                # Confirmar a transação
                connection.commit()

                print("Dados atualizados com sucesso.")

            except oracledb.DatabaseError as e:
                print("Erro ao atualizar os dados:", e)

            finally:
                # Fechar o cursor e a conexão
                cursor.close()
                connection.close()

# Função que busca o aluno pela matricula para montar a turma
def buscar_aluno_por_matricula(matricula):
    try:
        # Conectar ao banco de dados
        connection = oracledb.connect(
            user="rm97857",
            password="060105",
            dsn="oracle.fiap.com.br:1521/orcl"
        )

        # Criar um cursor
        cursor = connection.cursor()

        # Comando SQL para buscar o aluno pela matrícula na tabela 'cadastrop'
        sql_select = """
        SELECT apelido FROM cadastrop WHERE matricula = :matricula
        """  # Você pode querer retornar o apelido ou qualquer outro campo relevante
        
        # Adicione uma linha de depuração
        print(f"Buscando aluno na tabela 'cadastrop' com a matrícula: {matricula}")
        
        # Executar o comando de seleção
        cursor.execute(sql_select, matricula=matricula)
        
        # Obter o resultado
        aluno = cursor.fetchone()
        
        if aluno:
            return aluno[0]  # Retorna o apelido do aluno
        else:
            return None

    except oracledb.DatabaseError as e:
        print("Erro ao buscar aluno:", e)
        return None

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

# Função que exibe o DataFrame contendo os alunos cadastrados
def visualizar_usuarios_nao_autoridade():
    try:
        # Conectar ao banco de dados
        connection = oracledb.connect(
            user="rm97857",
            password="060105",
            dsn="oracle.fiap.com.br:1521/orcl"
        )

        # Criar um cursor
        cursor = connection.cursor()

        # Comando SQL para selecionar os usuários que não são autoridade, excluindo a senha
        sql_select = """
            SELECT email, apelido, cpf, matricula
            FROM cadastrop
            WHERE autoridade = 0
        """
        
        # Executar o comando de seleção
        cursor.execute(sql_select)
        
        # Buscar todos os resultados
        usuarios = cursor.fetchall()

        # Definir os nomes das colunas (sem a senha)
        colunas = ['Email', 'Apelido', 'CPF', 'Matrícula']

        # Criar um DataFrame a partir dos dados
        df = pd.DataFrame(usuarios, columns=colunas)

        # Exibir o DataFrame
        print("\n=== Alunos cadastrados ===")
        print(df)
        
    except oracledb.DatabaseError as e:
        print("Erro ao buscar os usuários:", e)

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

# Função para adicionar alunos à turma
def montar_turma():
    turma = []
    print("\n=== Montar Turma ===")
    
    while True:
        matricula_aluno = input("Digite a matrícula do aluno (ou 'sair' para finalizar): ")
        if matricula_aluno.lower() == 'sair':
            break
        
        # Buscar o aluno pelo banco de dados
        aluno_info = buscar_aluno_por_matricula(matricula_aluno)
        
        if aluno_info:
            apelido = aluno_info
            turma.append({"matricula": matricula_aluno, "nome": apelido})
            print(f"Aluno {apelido} (Matrícula: {matricula_aluno}, adicionado à turma.")
        else:
            print(f"Nenhum aluno encontrado com a matrícula {matricula_aluno}.")
    
    print("\nTurma montada com sucesso!")
    return turma  # Retornar a lista de alunos da turma

# Função que possibilita um professor cadastrado a ver as notas da turma
def ver_notas_turma(turma):
    if not turma:
        print("\nA turma está vazia. Nenhum aluno foi adicionado.")
        return
    
    print("\n=== Notas da Turma ===")
    
    try:
        # Conectar ao banco de dados
        connection = oracledb.connect(
            user="rm97857",
            password="060105",
            dsn="oracle.fiap.com.br:1521/orcl"
        )
        
        # Criar um cursor
        cursor = connection.cursor()
        
        # Percorrer a lista de alunos na turma para buscar as notas
        for aluno in turma:
            matricula = aluno['matricula']
            
            # Comando SQL para buscar a pontuação (nota) do aluno pela matrícula
            sql_select = """
            SELECT pontuacao FROM cadastrop WHERE matricula = :matricula
            """
            
            # Executar a busca
            cursor.execute(sql_select, matricula=matricula)
            pontuacao = cursor.fetchone()
            
            if pontuacao:
                print(f"Nome: {aluno['nome']}, Matrícula: {matricula}, Nota: {pontuacao[0]}")
            else:
                print(f"Nome: {aluno['nome']}, Matrícula: {matricula}, Nota: Não encontrada.")
    
    except oracledb.DatabaseError as e:
        print("Erro ao buscar notas dos alunos:", e)

# Função que simula uma conversa com a nossa IA, chamada Helena
def helena(dados_usuario):
    while True:
        print("\n=== Chat com a HELENA ===")
        print("\nOlá! Eu sou a HELENA, sua assistente virtual. Como posso ajudá-lo hoje?\n")
        print("1. Ver minha nota no teste de Laparoscopia")
        print("2. O que é o MyTeacher?")
        print("3. Informações sobre o desenvolvimento do jogo em realidade virtual")
        print("4. Sair")

        escolha = input("Escolha uma das opções: ")

        if escolha == '1':
            try:
                # Conectar ao banco de dados para buscar a nota do aluno
                connection = oracledb.connect(
                    user="rm97857",
                    password="060105",
                    dsn="oracle.fiap.com.br:1521/orcl"
                )
                cursor = connection.cursor()

                # Comando SQL para buscar a pontuação do aluno pela matrícula
                sql_select = """
                SELECT pontuacao FROM cadastrop WHERE matricula = :matricula
                """
                
                # Executar o comando de seleção
                cursor.execute(sql_select, matricula=dados_usuario['matricula'])
                
                # Obter o resultado
                pontuacao = cursor.fetchone()
                
                if pontuacao:
                    print(f"Sua nota no teste de Laparoscopia é de {pontuacao[0]}.")
                else:
                    print("Sua nota no teste de Laparoscopia não foi encontrada.")

            except oracledb.DatabaseError as e:
                print("Erro ao buscar a pontuação:", e)

            finally:
                cursor.close()
                connection.close()

        elif escolha == '2':
            print("\nO MyTeacher é uma plataforma inovadora de ensino que conecta alunos e professores no ambiente da medicina,\n oferecendo conteúdos interativos e testes práticos para aprimorar suas habilidades. \nAlém disso, conta com uma assistente virtual (eu!) e um sistema de pontuação para acompanhar seu progresso.\n")

        elif escolha == '3':
            print("\nO jogo que está em desenvolvimento vai simular procedimentos médicos em realidade virtual, focado especialmente \nem cirurgias laparoscópicas. Ele será uma ferramenta incrível para praticar e aprender em um ambiente seguro e imersivo.\n")

        elif escolha == '4':
            print("Saindo do chat com a HELENA.")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Função para a tela principal após o login
def tela_principal(dados_usuario):
    turma = []  # Variável local para armazenar a turma
    print("\nBem-vindo ao MyTeacher!")
    
    if dados_usuario['autoridade'] == 1:
        print("\nOlá professor!")  # Exibir "Bem-vindo, professor" para professores
    else:
        print("\nOlá aluno!")  # Exibir "Bem-vindo, aluno" para alunos
    
    while True:
        print("\nOpções:")
        print("1. Ver Perfil")
        print("2. Editar Dados")
        print("3. Conversar com a Helena")
        print("4. Conteúdos de Laparoscopia")
        print("5. Jogo em Realidade Virtual")
        print("6. Área de Saúde Mental")
        if dados_usuario['autoridade'] == 1: # Exibir as opções abaixo apenas para professores
            print("7. Montar Turma")  
            print("8. Ver notas da turma")  
            print("9. Ver tabela de alunos")
        print("10. Logout")
        
        escolha = input("Digite a opção desejada: ")
        
        if escolha == '1':
            print("\n=== Seu Perfil ===")
            print(f"Email: {dados_usuario['email']}")
            print(f"Apelido: {dados_usuario['apelido']}")
            print(f"CPF: {dados_usuario['cpf']}")
            print(f"Matrícula: {dados_usuario['matricula']}")
            print(f"Autoridade: {'Sim' if dados_usuario['autoridade'] == 1 else 'Não'}")
        
        elif escolha == '2':
            editar_dados_usuario(dados_usuario)
        
        elif escolha == '3' :
            helena(dados_usuario)

        elif escolha == '4' :
            while True:
                print("1. Os instrumentos da laparoscopia")
                print("2. Os procedimentos da laparoscopia")
                print("3. Videos")
                print("4. Sair")
                
                escolha_conteudo = input("Escolha uma das opções: ")

                if escolha_conteudo == '1':
                    print("Os principais instrumentos usados na laparoscopia são...\n\n")

                elif escolha_conteudo == '2':
                    print("Os principais procedimentos feitos na laparoscopia são...\n\n")

                elif escolha_conteudo == '3': 
                    print("aperte o play para iniciar o vídeo desejado:\n\n2")

                elif escolha_conteudo == '4': 
                    break

                else:
                    print("Escolha uma opção válida.")
        
        elif escolha == '5' :
                print("\nO jogo ainda está sendo desenvolvido, acesse nossa landing page no seu navegador para saber mais!\n")

        elif escolha == '6' :
                while True:
                    print("1. Mostrar psicólogos por perto")
                    print("2. Por que é importante médicos com a saúde mental em dia?")
                    print("3. Sair")

                    escolha_mental = input("Escolha uma das opções: ")

                    if escolha_mental == '1':
                        print("Psicólogos por perto: \n\n Marcos, atende presencialmente, atualmente a 3 km de sua localização \n\n Ana, atende de forma remota \n\n Caio, atende de forma remota \n")
                    
                    elif escolha_mental == '2':

                        print("A saúde mental no universo da medicina, é importante porque...")

                    elif escolha_mental == '3':
                        break
                

        elif escolha == '7' and dados_usuario['autoridade'] == 1:
            turma = montar_turma()  
        
        elif escolha == '8' and dados_usuario['autoridade'] == 1:
            ver_notas_turma(turma)  

        elif escolha == '9' and dados_usuario['autoridade'] == 1:
            visualizar_usuarios_nao_autoridade()
            
        elif escolha == '10':
            print("Saindo da Tela Principal.")
            break
        
        else:
            print("Opção inválida ou você não tem permissão para acessar esta opção. Tente novamente.")
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
                "autoridade": int(dados_usuario[4]) 
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

# Função principal do programa com o loop
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