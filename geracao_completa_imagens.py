#!/usr/bin/env python3
"""
Script para gerenciar a geração completa de todas as imagens faltantes
"""
import sqlite3
import os
import requests
from datetime import datetime

# Diretório das fotos
FOTOS_DIR = "static/img/itens"

# URLs das imagens já geradas (atualizar conforme geramos mais)
IMAGENS_GERADAS = {
    2: "https://im.runware.ai/image/ws/2/ii/d1269529-a977-44c2-8392-b5cce0eaa76c.jpg",   # Penteado de Noiva
    3: "https://im.runware.ai/image/ws/2/ii/e5862aaa-601f-4aae-935d-38800f9f82f4.jpg",   # Teste de Maquiagem
    4: "https://im.runware.ai/image/ws/2/ii/5741273a-2372-4a8b-abfd-698752c13d38.jpg",   # Maquiagem Madrinhas
    6: "https://im.runware.ai/image/ws/2/ii/0838394b-1fef-4399-8208-8b493377023b.jpg",   # Celebrante Religioso
    7: "https://im.runware.ai/image/ws/2/ii/b138f72d-c966-41d6-ac77-bdb4e919953e.jpg",   # Celebrante Bilíngue
    8: "https://im.runware.ai/image/ws/2/ii/924d4274-8eba-4cd8-bdbe-84288de32577.jpg",   # Celebrante Temático
    11: "https://im.runware.ai/image/ws/2/ii/01b449a4-8f3a-41ab-8229-3469bd4b1ab5.jpg",  # Doces Finos 100un
    12: "https://im.runware.ai/image/ws/2/ii/93dac8f6-a8dc-46e3-9bc5-a539be36ac5b.jpg",  # Naked Cake
    13: "https://im.runware.ai/image/ws/2/ii/a385b8b3-9da7-40ba-a09d-f8d9cb81ac60.jpg",  # Macarrons Franceses 100un
    14: "https://im.runware.ai/image/ws/2/ii/148b7588-3f24-425b-9a83-3e53d280dcad.jpg",  # Cupcakes Decorados 50un
    15: "https://im.runware.ai/image/ws/2/ii/802f4fdf-6e4f-4437-9d3f-2da79e979ca1.jpg",  # Torre de Profiteroles
    16: "https://im.runware.ai/image/ws/2/ii/687d3cd9-51c5-46c0-860b-d27820e2d394.jpg",  # Brigadeiros Gourmet 100un
    18: "https://im.runware.ai/image/ws/2/ii/25ca460a-cd29-456d-afbc-cca506264d7e.jpg",  # Segurança VIP
    19: "https://im.runware.ai/image/ws/2/ii/580b69e7-4c86-45ae-bdb6-ea65a7ad1e45.jpg",  # Detector de Metais
    20: "https://im.runware.ai/image/ws/2/ii/f5ee624c-c452-47ce-a0da-f91812ca5e43.jpg",  # Brigadista
    27: "https://im.runware.ai/image/ws/2/ii/20399e8d-d366-4b1a-b16a-253fd3435214.jpg",  # Capela Ecumênica
    29: "https://im.runware.ai/image/ws/2/ii/be314235-439f-4667-b07f-8e2cef8c2fcf.jpg",  # Cerimonial Cerimônia
    30: "https://im.runware.ai/image/ws/2/ii/7df26d83-fe59-472d-8f71-be15bba8cc95.jpg",  # Day-of Coordinator
    31: "https://im.runware.ai/image/ws/2/ii/882ace9d-e130-453b-93df-88dfbd3a599e.jpg",  # Planejamento 12 Meses
    32: "https://im.runware.ai/image/ws/2/ii/c2b55743-17d3-46df-af9e-34688ce15771.jpg",  # Consultoria por Hora
    36: "https://im.runware.ai/image/ws/2/ii/96ce7200-4632-41ce-a5b3-2eb63e3e456e.jpg",  # Salão de Festas 100 pessoas
    39: "https://im.runware.ai/image/ws/2/ii/2b136a28-3649-4f57-b03c-2be369b5fba7.jpg",  # Vestido de Noiva Sereia
    40: "https://im.runware.ai/image/ws/2/ii/da53cb75-87b7-47f8-b834-37aad0d169fd.jpg",  # Sapato de Noiva Perolado
    42: "https://im.runware.ai/image/ws/2/ii/889eaebb-5a4a-43b1-9e34-88b1c9f732c3.jpg",  # Quarto Standard
    43: "https://im.runware.ai/image/ws/2/ii/7af332d8-796f-478b-9ddb-bf450467eb87.jpg",  # Pacote Weekend
    50: "https://im.runware.ai/image/ws/2/ii/95a9433f-b290-45c2-99b7-f3c1f831b043.jpg",  # Cobertura Completa do Casamento
    51: "https://im.runware.ai/image/ws/2/ii/a8df87ec-aaeb-4c9c-a1b0-46253080abbf.jpg",  # Vídeo Highlights
    52: "https://im.runware.ai/image/ws/2/ii/93d9b823-9c0b-4d8b-89ff-ffb8c2b09ca2.jpg",  # Álbum Premium 30x30
    53: "https://im.runware.ai/image/ws/2/ii/883acb36-b78a-4c8e-b0f0-ae2787140d7f.jpg",  # Drone Aéreo
    54: "https://im.runware.ai/image/ws/2/ii/a91dd061-f9d3-4940-9438-6018ee9fcc9f.jpg",  # Impressão Fine Art
}

def log_action(message):
    """Registra ações no log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def obter_itens_sem_fotos():
    """Obtém lista de itens que ainda precisam de fotos"""
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT i.id, i.nome, i.descricao, i.preco, c.nome as categoria, i.tipo
        FROM item i
        LEFT JOIN categoria c ON i.id_categoria = c.id
        ORDER BY i.id
    ''')

    todos_itens = cursor.fetchall()
    conn.close()

    itens_sem_fotos = []
    for item in todos_itens:
        item_id = item[0]
        foto_nome = f"{item_id:06d}.jpg"
        foto_path = os.path.join(FOTOS_DIR, foto_nome)

        # Se não tem foto física E não está na lista de geradas
        if not os.path.exists(foto_path) and item_id not in IMAGENS_GERADAS:
            itens_sem_fotos.append(item)

    return itens_sem_fotos

def baixar_imagem(url, caminho_destino):
    """Baixa uma imagem de uma URL e salva no caminho especificado"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(caminho_destino, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                arquivo.write(chunk)

        return True
    except Exception as e:
        log_action(f"❌ Erro ao baixar {url}: {e}")
        return False

def baixar_imagens_pendentes():
    """Baixa todas as imagens que foram geradas mas ainda não baixadas"""
    log_action("📥 Baixando imagens pendentes...")

    if not os.path.exists(FOTOS_DIR):
        os.makedirs(FOTOS_DIR)

    baixadas = 0
    for item_id, url in IMAGENS_GERADAS.items():
        nome_arquivo = f"{item_id:06d}.jpg"
        caminho_destino = os.path.join(FOTOS_DIR, nome_arquivo)

        if not os.path.exists(caminho_destino):
            log_action(f"📥 Baixando item {item_id}: {nome_arquivo}")
            if baixar_imagem(url, caminho_destino):
                log_action(f"✅ Salvo: {nome_arquivo}")
                baixadas += 1
        else:
            log_action(f"✓ Já existe: {nome_arquivo}")

    return baixadas

def gerar_relatorio():
    """Gera relatório do progresso atual"""
    log_action("📊 Gerando relatório de progresso...")

    # Contar fotos existentes
    fotos_existentes = 0
    if os.path.exists(FOTOS_DIR):
        fotos_existentes = len([f for f in os.listdir(FOTOS_DIR) if f.endswith('.jpg')])

    # Contar itens sem fotos
    itens_sem_fotos = obter_itens_sem_fotos()

    # Contar imagens geradas mas não baixadas
    imagens_pendentes = 0
    for item_id in IMAGENS_GERADAS:
        nome_arquivo = f"{item_id:06d}.jpg"
        caminho = os.path.join(FOTOS_DIR, nome_arquivo)
        if not os.path.exists(caminho):
            imagens_pendentes += 1

    log_action(f"📸 Fotos existentes no diretório: {fotos_existentes}")
    log_action(f"🔄 Imagens geradas mas não baixadas: {imagens_pendentes}")
    log_action(f"⏳ Itens ainda precisando de imagens: {len(itens_sem_fotos)}")
    log_action(f"📈 Total de imagens já geradas: {len(IMAGENS_GERADAS)}")

    if itens_sem_fotos:
        log_action("📋 Próximos itens a serem gerados:")
        for i, item in enumerate(itens_sem_fotos[:10], 1):
            item_id, nome, desc, preco, categoria, tipo = item
            log_action(f"  {i:2d}. ID {item_id:3d}: {nome} ({categoria})")

def main():
    """Função principal"""
    log_action("🚀 Iniciando gerenciamento de imagens")

    # Baixar imagens pendentes
    baixadas = baixar_imagens_pendentes()
    log_action(f"✅ {baixadas} imagens baixadas")

    # Gerar relatório
    gerar_relatorio()

if __name__ == "__main__":
    main()