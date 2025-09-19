from typing import Optional
from model.usuario_model import Usuario, TipoUsuario
from repo import usuario_repo, fornecedor_repo, casal_repo, item_repo, categoria_item_repo, fornecedor_item_repo, item_demanda_repo, item_orcamento_repo
from util.security import criar_hash_senha

def criar_admin_padrao() -> Optional[int]:
    """
    Cria um administrador padrão se não existir nenhum admin no sistema.
    Retorna o ID do admin criado ou None se já existir um admin.
    """
    try:
        # Criar todas as tabelas necessárias
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        casal_repo.criar_tabela_casal()
        item_repo.criar_tabela_item()
        categoria_item_repo.criar_tabela_categoria_item()
        fornecedor_item_repo.criar_tabela_fornecedor_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_orcamento_repo.criar_tabela_item_orcamento()

        # Buscar por um admin existente (simplificado - seria melhor ter uma query específica)
        # Por ora, vamos verificar se existe um usuário com email admin específico
        admin_existente = usuario_repo.obter_usuario_por_email("admin@casebem.com")

        if admin_existente:
            print("✅ Administrador já existe no sistema")
            return admin_existente.id

        # Criar administrador padrão
        senha_hash = criar_hash_senha("admin123")  # Senha padrão - deve ser alterada no primeiro login

        admin = Usuario(
            id=0,
            nome="Administrador",
            cpf=None,
            data_nascimento=None,
            email="admin@casebem.com",
            telefone="(28) 99999-0000",
            senha=senha_hash,
            perfil=TipoUsuario.ADMIN,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )

        admin_id = usuario_repo.inserir_usuario(admin)

        if admin_id:
            print(f"✅ Administrador padrão criado com sucesso! ID: {admin_id}")
            print("📧 Email: admin@casebem.com")
            print("🔑 Senha: admin123")
            print("⚠️  IMPORTANTE: Altere a senha no primeiro login!")
            return admin_id
        else:
            print("❌ Erro ao criar administrador padrão")
            return None

    except Exception as e:
        print(f"❌ Erro ao verificar/criar administrador: {e}")
        return None

def inicializar_sistema():
    """
    Inicializa o sistema executando todas as verificações e configurações necessárias.
    """
    print("🚀 Inicializando sistema CaseBem...")

    # Criar administrador padrão se necessário
    criar_admin_padrao()

    print("✅ Sistema inicializado com sucesso!")