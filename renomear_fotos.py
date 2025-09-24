#!/usr/bin/env python3
"""
Script para renomear fotos dos itens de acordo com o mapeamento entre dados2.db e dados.db
"""
import os
import shutil
from datetime import datetime

# Diretório das fotos
FOTOS_DIR = "static/img/itens"

# Mapeamento completo: dados2.db ID -> dados.db ID
MAPEAMENTO = {
    1: 92,   # Decoração Completa
    2: 21,   # Buquê de Noiva Rosas
    3: 22,   # Boutonnière para Noivo
    4: 23,   # Corsage para Madrinhas
    5: 24,   # Buquê de Noiva Peônias
    6: 89,   # Limpeza Pós-Evento
    7: 1,    # Maquiagem de Noiva
    8: 63,   # DJ para Cerimônia
    9: 95,   # Van para Convidados
    10: 96,  # Carro Antigo Conversível
    11: 97,  # Limousine Branca
    12: 17,  # Segurança Particular
    13: 56,  # Vinho Tinto Seleção
    14: 57,  # Caipirinha Bar
    15: 41,  # Suíte Presidencial
    16: 37,  # Véu de Noiva 3 metros
    17: 38,  # Vestido de Noiva Princesa
    18: 28,  # Cerimonial Completo
    19: 48,  # Filmagem Cerimônia
    20: 49,  # Ensaio Pré-Wedding
    21: 25,  # Gazebo para Cerimônia
    22: 26,  # Jardim para Cerimônia
    23: 77,  # Convite Clássico 100un
    24: 78,  # Save the Date 100un
    25: 79,  # Lembrancinha Sabonete 100un
    26: 33,  # Salão de Festas 150 pessoas
    27: 34,  # Espaço Gourmet
    28: 35,  # Sala de Noiva
    29: 5,   # Celebrante Civil
    30: 71,  # Cadeira Tiffany
    31: 72,  # Mesa Redonda 8 pessoas
    32: 9,   # Bem-Casados 100un
    33: 10,  # Bolo de Casamento 3 andares
    34: 81,  # Mesa de Doces Finos
    35: 82,  # Buffet Completo 150 pessoas
    36: 83,  # Bar Premium
    37: 84,  # Buffet Completo 100 pessoas
    38: 44,  # Brincos de Pérola
    39: 45,  # Anel de Noivado Solitário
    40: 46,  # Aliança Ouro 18k Lisa
    41: 47,  # Aliança com Diamante
}

def log_action(message):
    """Registra ações no log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_conflitos():
    """Identifica quais renomeações causarão conflitos"""
    conflitos = []
    for old_id, new_id in MAPEAMENTO.items():
        old_file = f"000{old_id:03d}.jpg"
        new_file = f"000{new_id:03d}.jpg"

        # Se o arquivo de destino já existe E não é o mesmo arquivo origem
        if os.path.exists(os.path.join(FOTOS_DIR, new_file)) and old_id != new_id:
            conflitos.append((old_id, new_id))

    return conflitos

def fase1_renomear_conflitantes():
    """FASE 1: Renomear fotos conflitantes para nomes temporários"""
    log_action("=== INICIANDO FASE 1: Renomear conflitantes ===")

    conflitos = get_conflitos()
    log_action(f"Identificados {len(conflitos)} conflitos")

    for old_id, new_id in conflitos:
        old_file = f"000{old_id:03d}.jpg"
        temp_file = f"temp_{old_id:03d}_to_{new_id:03d}.jpg"

        old_path = os.path.join(FOTOS_DIR, old_file)
        temp_path = os.path.join(FOTOS_DIR, temp_file)

        if os.path.exists(old_path):
            shutil.move(old_path, temp_path)
            log_action(f"✓ {old_file} → {temp_file}")
        else:
            log_action(f"⚠ {old_file} não encontrado")

    log_action("✅ FASE 1 concluída")

def fase2_renomear_sem_conflito():
    """FASE 2: Renomear fotos sem conflito para destino final"""
    log_action("=== INICIANDO FASE 2: Renomear sem conflito ===")

    conflitos_ids = [old_id for old_id, _ in get_conflitos()]
    sem_conflito = 0

    for old_id, new_id in MAPEAMENTO.items():
        if old_id not in conflitos_ids:
            old_file = f"000{old_id:03d}.jpg"
            new_file = f"000{new_id:03d}.jpg"

            old_path = os.path.join(FOTOS_DIR, old_file)
            new_path = os.path.join(FOTOS_DIR, new_file)

            if os.path.exists(old_path):
                shutil.move(old_path, new_path)
                log_action(f"✓ {old_file} → {new_file}")
                sem_conflito += 1
            else:
                log_action(f"⚠ {old_file} não encontrado")

    log_action(f"✅ FASE 2 concluída - {sem_conflito} arquivos renomeados")

def fase3_renomear_temporarios():
    """FASE 3: Renomear arquivos temporários para destino final"""
    log_action("=== INICIANDO FASE 3: Renomear temporários ===")

    temporarios = 0

    # Listar arquivos temporários
    for filename in os.listdir(FOTOS_DIR):
        if filename.startswith("temp_") and filename.endswith(".jpg"):
            # Extrair IDs do nome temporário
            parts = filename.replace("temp_", "").replace(".jpg", "").split("_to_")
            if len(parts) == 2:
                old_id = int(parts[0])
                new_id = int(parts[1])

                temp_path = os.path.join(FOTOS_DIR, filename)
                new_file = f"000{new_id:03d}.jpg"
                new_path = os.path.join(FOTOS_DIR, new_file)

                shutil.move(temp_path, new_path)
                log_action(f"✓ {filename} → {new_file}")
                temporarios += 1

    log_action(f"✅ FASE 3 concluída - {temporarios} arquivos temporários renomeados")

def validar_resultado():
    """Valida se todas as fotos foram renomeadas corretamente"""
    log_action("=== VALIDANDO RESULTADO ===")

    # Verificar se todas as fotos esperadas existem
    encontradas = 0
    faltando = []

    for old_id, new_id in MAPEAMENTO.items():
        new_file = f"000{new_id:03d}.jpg"
        new_path = os.path.join(FOTOS_DIR, new_file)

        if os.path.exists(new_path):
            encontradas += 1
        else:
            faltando.append((old_id, new_id, new_file))

    log_action(f"✓ Fotos encontradas: {encontradas}/41")

    if faltando:
        log_action("❌ Fotos faltando:")
        for old_id, new_id, new_file in faltando:
            log_action(f"   {old_id:3d} → {new_id:3d} ({new_file})")

    # Verificar se restaram arquivos temporários
    temporarios = [f for f in os.listdir(FOTOS_DIR) if f.startswith("temp_")]
    if temporarios:
        log_action("❌ Arquivos temporários restantes:")
        for temp in temporarios:
            log_action(f"   {temp}")
    else:
        log_action("✓ Nenhum arquivo temporário restante")

    # Verificar arquivo svg
    svg_path = os.path.join(FOTOS_DIR, "ph-sem-foto.svg")
    if os.path.exists(svg_path):
        log_action("✓ ph-sem-foto.svg preservado")
    else:
        log_action("⚠ ph-sem-foto.svg não encontrado")

    if encontradas == 41 and not faltando and not temporarios:
        log_action("✅ VALIDAÇÃO PASSOU - Todas as fotos foram renomeadas corretamente!")
        return True
    else:
        log_action("❌ VALIDAÇÃO FALHOU - Existem problemas na renomeação")
        return False

def main():
    """Executa o processo completo de renomeação"""
    log_action("🚀 Iniciando renomeação de fotos dos itens")
    log_action(f"Diretório: {FOTOS_DIR}")
    log_action(f"Total de mapeamentos: {len(MAPEAMENTO)}")

    try:
        # Verificar se diretório existe
        if not os.path.exists(FOTOS_DIR):
            log_action(f"❌ Diretório {FOTOS_DIR} não existe!")
            return

        # Executar as 3 fases
        fase1_renomear_conflitantes()
        fase2_renomear_sem_conflito()
        fase3_renomear_temporarios()

        # Validar resultado
        sucesso = validar_resultado()

        if sucesso:
            log_action("🎉 Renomeação concluída com sucesso!")
        else:
            log_action("💥 Renomeação concluída com problemas!")

    except Exception as e:
        log_action(f"❌ Erro durante a renomeação: {e}")

if __name__ == "__main__":
    main()