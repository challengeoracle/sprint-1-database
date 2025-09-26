import oracledb
import random
from faker import Faker
from datetime import datetime

# --- CONFIGURAÇÕES DE CONEXÃO ---
# Substitua com suas credenciais do banco de dados Oracle
DB_USER = "" # ADICIONAR O RM
DB_PASSWORD = "" # ADICIONAR A SENHA
DB_DSN = "oracle.fiap.com.br:1521/ORCL"

# Inicializa o Faker para gerar dados fictícios
fake = Faker('pt_BR')

def conectar_banco():
    """Estabelece a conexão com o banco de dados Oracle."""
    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        print("Conexão com o banco de dados Oracle bem-sucedida!")
        return connection
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None

def inserir_dados(connection):
    """Insere exatamente 10 registros de exemplo em todas as tabelas usando dados pré-definidos."""
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Listas para armazenar os IDs gerados
        ids_unidades = []
        ids_usuarios_pacientes = []
        ids_usuarios_colaboradores = []
        ids_especialidades = []
        ids_pacientes = []
        ids_colaboradores = []
        ids_recursos = []
        
        print("\n--- Iniciando inserção de dados ---")
        
        # 1. UNIDADES DE SAÚDE (10 registros) - Dados pré-definidos
        print("Inserindo 10 Unidades de Saúde...")
        unidades = [
            ('Hospital Sírio-Libanês', '58509433000184', 'Rua Dona Adma Jafet, 91', 'HOSPITAL'),
            ('Clínica Fares', '01128543000100', 'Av. Jabaquara, 123', 'CLÍNICA'),
            ('Laboratório Fleury', '60840055000131', 'Av. Brasil, 2000', 'LABORATÓRIO'),
            ('Hospital Albert Einstein', '60765823000130', 'Av. Albert Einstein, 627', 'HOSPITAL'),
            ('Clínica de Olhos Dr. Visão', '12345678000199', 'Rua da Oftalmologia, 100', 'CLÍNICA'),
            ('Laboratório A+', '09368383000100', 'Av. Santo Amaro, 2300', 'LABORATÓRIO'),
            ('Hospital das Clínicas', '46371729000104', 'Av. Dr. Enéas de Carvalho Aguiar, 255', 'HOSPITAL'),
            ('Centro Médico Pirituba', '98765432000111', 'Av. Mutinga, 500', 'CLÍNICA'),
            ('Hospital Infantil Sabará', '61192935000171', 'Av. Angélica, 1987', 'HOSPITAL'),
            ('DASA Laboratórios', '61486650000183', 'Alphaville, Barueri', 'LABORATÓRIO')
        ]
        sql_unidade = "INSERT INTO TB_MEDI_UNIDADE_SAUDE (dt_criacao, nm_unidade, nr_cnpj, ds_endereco, tp_unidade) VALUES (:1, :2, :3, :4, :5) RETURNING id_unidade_saude INTO :6"
        for unidade in unidades:
            id_var = cursor.var(oracledb.NUMBER)
            cursor.execute(sql_unidade, (datetime.now(), unidade[0], unidade[1], unidade[2], unidade[3], id_var))
            ids_unidades.append(id_var.getvalue()[0])

        # 2. USUÁRIOS (20 registros no total para popular as outras tabelas)
        print("Inserindo 20 Usuários (10 para Pacientes, 10 para Colaboradores)...")
        
        pacientes_data = [
            {'nome': 'Carlos Santana', 'email': 'carlos.santana@email.com', 'cpf': '11122233344'},
            {'nome': 'Ana Carolina', 'email': 'ana.carolina@email.com', 'cpf': '22233344455'},
            {'nome': 'Beatriz Costa', 'email': 'beatriz.costa@email.com', 'cpf': '33344455566'},
            {'nome': 'Daniel Alves', 'email': 'daniel.alves@email.com', 'cpf': '44455566677'},
            {'nome': 'Eduarda Lima', 'email': 'eduarda.lima@email.com', 'cpf': '55566677788'},
            {'nome': 'Fábio Junior', 'email': 'fabio.junior@email.com', 'cpf': '66677788899'},
            {'nome': 'Gabriela Ferreira', 'email': 'gabriela.ferreira@email.com', 'cpf': '77788899900'},
            {'nome': 'Heitor Martins', 'email': 'heitor.martins@email.com', 'cpf': '88899900011'},
            {'nome': 'Isabela Gomes', 'email': 'isabela.gomes@email.com', 'cpf': '99900011122'},
            {'nome': 'João Pereira', 'email': 'joao.pereira@email.com', 'cpf': '00011122233'}
        ]

        colaboradores_data = [
            {'nome': 'Dr. Ricardo Neves', 'email': 'ricardo.neves@medix.com', 'cpf': '12312312311'},
            {'nome': 'Enf. Mônica Barros', 'email': 'monica.barros@medix.com', 'cpf': '23423423422'},
            {'nome': 'Admin. Lucas Souza', 'email': 'lucas.souza@medix.com', 'cpf': '34534534533'},
            {'nome': 'Rec. Patrícia Andrade', 'email': 'patricia.andrade@medix.com', 'cpf': '45645645644'},
            {'nome': 'Dra. Fernanda Rocha', 'email': 'fernanda.rocha@medix.com', 'cpf': '56756756755'},
            {'nome': 'Enf. Rafael Oliveira', 'email': 'rafael.oliveira@medix.com', 'cpf': '67867867866'},
            {'nome': 'Dr. Bruno Mendes', 'email': 'bruno.mendes@medix.com', 'cpf': '78978978977'},
            {'nome': 'Admin. Vanessa Dias', 'email': 'vanessa.dias@medix.com', 'cpf': '89089089088'},
            {'nome': 'Dra. Camila Ribeiro', 'email': 'camila.ribeiro@medix.com', 'cpf': '90190190199'},
            {'nome': 'Enf. Tiago Santos', 'email': 'tiago.santos@medix.com', 'cpf': '01201201200'}
        ]

        sql_usuario = "INSERT INTO TB_MEDI_USUARIO (dt_criacao, nm_usuario, ds_email, ds_senha_hash, nr_cpf, tp_usuario) VALUES (:1, :2, :3, :4, :5, :6) RETURNING id_usuario INTO :7"
        
        for p_data in pacientes_data:
            id_usuario_var = cursor.var(oracledb.NUMBER)
            cursor.execute(sql_usuario, (datetime.now(), p_data['nome'], p_data['email'], fake.password(), p_data['cpf'], 'PACIENTE', id_usuario_var))
            ids_usuarios_pacientes.append(id_usuario_var.getvalue()[0])

        for c_data in colaboradores_data:
            id_usuario_var = cursor.var(oracledb.NUMBER)
            cursor.execute(sql_usuario, (datetime.now(), c_data['nome'], c_data['email'], fake.password(), c_data['cpf'], 'COLABORADOR', id_usuario_var))
            ids_usuarios_colaboradores.append(id_usuario_var.getvalue()[0])
            
        # 3. PACIENTES (10 registros)
        print("Inserindo 10 Pacientes...")
        for id_usuario in ids_usuarios_pacientes:
            sql_paciente = "INSERT INTO TB_MEDI_PACIENTE (dt_criacao, id_usuario, dt_nascimento, nr_convenio) VALUES (:1, :2, :3, :4) RETURNING id_paciente INTO :5"
            id_paciente_var = cursor.var(oracledb.NUMBER)
            cursor.execute(sql_paciente, (datetime.now(), id_usuario, fake.date_of_birth(minimum_age=1, maximum_age=90), fake.random_number(digits=10, fix_len=True), id_paciente_var))
            ids_pacientes.append(id_paciente_var.getvalue()[0])

        # 4. COLABORADORES (10 registros)
        print("Inserindo 10 Colaboradores...")
        cargos = ['MÉDICO', 'ENFERMEIRO', 'ADMINISTRATIVO', 'RECEPCIONISTA', 'MÉDICO', 'ENFERMEIRO', 'MÉDICO', 'ADMINISTRATIVO', 'MÉDICO', 'ENFERMEIRO']
        for i, id_usuario in enumerate(ids_usuarios_colaboradores):
            sql_colaborador = "INSERT INTO TB_MEDI_COLABORADOR (dt_criacao, id_usuario, id_unidade_saude, ds_cargo) VALUES (:1, :2, :3, :4) RETURNING id_colaborador INTO :5"
            id_colaborador_var = cursor.var(oracledb.NUMBER)
            unidade_aleatoria = random.choice(ids_unidades)
            cursor.execute(sql_colaborador, (datetime.now(), id_usuario, unidade_aleatoria, cargos[i], id_colaborador_var))
            ids_colaboradores.append(id_colaborador_var.getvalue()[0])

        # 5. ESPECIALIDADES (10 registros)
        print("Inserindo 10 Especialidades...")
        especialidades = ['CARDIOLOGIA', 'PEDIATRIA', 'ORTOPEDIA', 'CLÍNICA GERAL', 'DERMATOLOGIA', 'GINECOLOGIA', 'NEUROLOGIA', 'PSIQUIATRIA', 'RADIOLOGIA', 'UROLOGIA']
        sql_especialidade = "INSERT INTO TB_MEDI_ESPECIALIDADE (dt_criacao, nm_especialidade) VALUES (:1, :2) RETURNING id_especialidade INTO :3"
        for esp in especialidades:
            id_var = cursor.var(oracledb.NUMBER)
            cursor.execute(sql_especialidade, (datetime.now(), esp, id_var))
            ids_especialidades.append(id_var.getvalue()[0])

        # 6. COLABORADOR_ESPECIALIDADE (10 registros)
        print("Vinculando 10 especialidades a 10 colaboradores...")
        sql_col_esp = "INSERT INTO TB_MEDI_COLABORADOR_ESPECIALIDADE (dt_criacao, id_colaborador, id_especialidade) VALUES (:1, :2, :3)"
        for i in range(10):
            cursor.execute(sql_col_esp, (datetime.now(), ids_colaboradores[i], ids_especialidades[i]))

        # 7. RECURSOS (10 registros)
        print("Inserindo 10 Recursos...")
        sql_recurso = "INSERT INTO TB_MEDI_RECURSO (dt_criacao, id_unidade_saude, nm_recurso, tp_recurso, st_recurso) VALUES (:1, :2, :3, :4, :5) RETURNING id_recurso INTO :6"
        for i in range(10):
            tipos_recurso = ['LEITO', 'CONSULTÓRIO', 'EQUIPAMENTO', 'SALA_CIRURGIA']
            status_recurso = ['Disponível', 'Ocupado', 'Manutenção']
            tipo = random.choice(tipos_recurso)
            nome_recurso = f"{tipo.capitalize().replace('_', ' ')} {random.randint(101, 599)}"
            id_var = cursor.var(oracledb.NUMBER)
            unidade_aleatoria = random.choice(ids_unidades)
            cursor.execute(sql_recurso, (datetime.now(), unidade_aleatoria, nome_recurso, tipo, random.choice(status_recurso), id_var))
            ids_recursos.append(id_var.getvalue()[0])
        
        # 8. AGENDAMENTOS (10 registros)
        print("Inserindo 10 Agendamentos...")
        sql_agendamento = "INSERT INTO TB_MEDI_AGENDAMENTO (dt_criacao, id_paciente, id_colaborador, id_recurso, id_unidade_saude, dt_hr_inicio, tp_agendamento, st_agendamento, dt_atualizacao) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)"
        for _ in range(10): 
            paciente = random.choice(ids_pacientes)
            colaborador = random.choice(ids_colaboradores)
            recurso = random.choice(ids_recursos)
            tipos_agendamento = ['CONSULTA', 'INTERNACAO', 'EXAME']
            status_agendamento = ['Agendado', 'Realizado', 'Cancelado']
            
            cursor.execute("SELECT id_unidade_saude FROM TB_MEDI_COLABORADOR WHERE id_colaborador = :id", id=colaborador)
            id_unidade_col = cursor.fetchone()[0]
            
            data_inicio = fake.future_datetime(end_date="+30d")
            now = datetime.now()
            
            cursor.execute(sql_agendamento, (now, paciente, colaborador, recurso, id_unidade_col, data_inicio, random.choice(tipos_agendamento), random.choice(status_agendamento), now))

        connection.commit()
        print("\n--- Inserção de dados concluída com sucesso! ---")

    except oracledb.DatabaseError as e:
        print(f"Erro durante a inserção de dados: {e}")
        connection.rollback()
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = conectar_banco()
    if conn:
        inserir_dados(conn)
        conn.close()
        print("\nConexão com o banco de dados fechada.")

