#!/usr/bin/env python3
"""
Script para baixar e salvar imagens geradas para os itens
"""
import requests
import os
from datetime import datetime

# Diretório das fotos
FOTOS_DIR = "static/img/itens"

# Mapeamento das imagens geradas: ID do item -> URL da imagem
IMAGENS_GERADAS = {
    2: "https://im.runware.ai/image/ws/2/ii/d1269529-a977-44c2-8392-b5cce0eaa76c.jpg",  # Penteado de Noiva
    3: "https://im.runware.ai/image/ws/2/ii/e5862aaa-601f-4aae-935d-38800f9f82f4.jpg",  # Teste de Maquiagem
    4: "https://im.runware.ai/image/ws/2/ii/5741273a-2372-4a8b-abfd-698752c13d38.jpg",  # Maquiagem Madrinhas
    6: "https://im.runware.ai/image/ws/2/ii/0838394b-1fef-4399-8208-8b493377023b.jpg",  # Celebrante Religioso
    7: "https://im.runware.ai/image/ws/2/ii/b138f72d-c966-41d6-ac77-bdb4e919953e.jpg",  # Celebrante Bilíngue
    8: "https://im.runware.ai/image/ws/2/ii/924d4274-8eba-4cd8-bdbe-84288de32577.jpg",  # Celebrante Temático
    11: "https://im.runware.ai/image/ws/2/ii/01b449a4-8f3a-41ab-8229-3469bd4b1ab5.jpg", # Doces Finos 100un
    12: "https://im.runware.ai/image/ws/2/ii/93dac8f6-a8dc-46e3-9bc5-a539be36ac5b.jpg", # Naked Cake
    13: "https://im.runware.ai/image/ws/2/ii/a385b8b3-9da7-40ba-a09d-f8d9cb81ac60.jpg", # Macarrons Franceses 100un
    14: "https://im.runware.ai/image/ws/2/ii/148b7588-3f24-425b-9a83-3e53d280dcad.jpg", # Cupcakes Decorados 50un
    15: "https://im.runware.ai/image/ws/2/ii/802f4fdf-6e4f-4437-9d3f-2da79e979ca1.jpg", # Torre de Profiteroles
    16: "https://im.runware.ai/image/ws/2/ii/687d3cd9-51c5-46c0-860b-d27820e2d394.jpg", # Brigadeiros Gourmet 100un
}

def log_action(message):
    """Registra ações no log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

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

def baixar_todas_imagens():
    """Baixa todas as imagens já geradas"""
    log_action("🚀 Iniciando download das imagens geradas")

    if not os.path.exists(FOTOS_DIR):
        os.makedirs(FOTOS_DIR)

    sucesso = 0
    falha = 0

    for item_id, url in IMAGENS_GERADAS.items():
        nome_arquivo = f"{item_id:06d}.jpg"
        caminho_destino = os.path.join(FOTOS_DIR, nome_arquivo)

        log_action(f"📥 Baixando item {item_id}: {nome_arquivo}")

        if baixar_imagem(url, caminho_destino):
            log_action(f"✅ Salvo: {nome_arquivo}")
            sucesso += 1
        else:
            log_action(f"❌ Falha: {nome_arquivo}")
            falha += 1

    log_action(f"📊 Resultado: {sucesso} sucessos, {falha} falhas")
    return sucesso, falha

if __name__ == "__main__":
    baixar_todas_imagens()