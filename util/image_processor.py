"""
Processador centralizado de imagens para o sistema CaseBem.

Este módulo elimina a duplicação de código de processamento de imagens
que estava espalhada em múltiplas rotas.
"""

from typing import Tuple, Optional
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
import os


class ImageProcessor:
    """Processador centralizado de imagens com validação e redimensionamento"""

    # Tipos de arquivo permitidos
    TIPOS_PERMITIDOS = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    # Tamanho máximo em MB
    TAMANHO_MAXIMO_MB = 5
    TAMANHO_MAXIMO_BYTES = TAMANHO_MAXIMO_MB * 1024 * 1024

    # Qualidade padrão para compressão JPEG
    QUALIDADE_PADRAO = 85

    @staticmethod
    async def processar_e_salvar_imagem(
        arquivo_upload: UploadFile,
        caminho_destino: str,
        tamanho: Tuple[int, int] = (600, 600),
        qualidade: int = QUALIDADE_PADRAO
    ) -> Tuple[bool, Optional[str]]:
        """
        Processa e salva imagem com validação e redimensionamento.

        Args:
            arquivo_upload: Arquivo enviado pelo usuário
            caminho_destino: Caminho onde a imagem será salva
            tamanho: Tupla (largura, altura) para redimensionamento
            qualidade: Qualidade da compressão JPEG (0-100)

        Returns:
            Tuple[bool, Optional[str]]: (sucesso, mensagem_erro)
                - (True, None) se sucesso
                - (False, "mensagem de erro") se falha
        """
        # Validar tipo de arquivo
        if arquivo_upload.content_type not in ImageProcessor.TIPOS_PERMITIDOS:
            tipos_formatados = ", ".join([t.split("/")[1].upper() for t in ImageProcessor.TIPOS_PERMITIDOS])
            return False, f"Tipo de arquivo inválido. Use: {tipos_formatados}"

        # Ler conteúdo do arquivo
        try:
            conteudo = await arquivo_upload.read()
        except Exception as e:
            return False, f"Erro ao ler arquivo: {str(e)}"

        # Validar tamanho
        tamanho_mb = len(conteudo) / (1024 * 1024)
        if len(conteudo) > ImageProcessor.TAMANHO_MAXIMO_BYTES:
            return False, f"Arquivo muito grande ({tamanho_mb:.1f}MB). Máximo permitido: {ImageProcessor.TAMANHO_MAXIMO_MB}MB"

        try:
            # Abrir imagem com PIL
            imagem_bytes = BytesIO(conteudo)
            imagem = Image.open(imagem_bytes)

            # Converter para RGB se necessário (RGBA ou P precisam ser convertidos)
            if imagem.mode in ("RGBA", "P"):
                imagem = imagem.convert("RGB")

            # Redimensionar mantendo proporção
            imagem.thumbnail(tamanho, Image.Resampling.LANCZOS)

            # Criar imagem quadrada com fundo branco
            imagem_quadrada = Image.new("RGB", tamanho, (255, 255, 255))

            # Centralizar a imagem redimensionada no quadrado
            x = (tamanho[0] - imagem.width) // 2
            y = (tamanho[1] - imagem.height) // 2
            imagem_quadrada.paste(imagem, (x, y))

            # Criar diretório se não existir
            diretorio = os.path.dirname(caminho_destino)
            if diretorio:
                os.makedirs(diretorio, exist_ok=True)

            # Salvar como JPEG com compressão
            imagem_quadrada.save(caminho_destino, "JPEG", quality=qualidade, optimize=True)

            return True, None

        except Exception as e:
            return False, f"Erro ao processar imagem: {str(e)}"

    @staticmethod
    def validar_arquivo(arquivo: UploadFile) -> Tuple[bool, Optional[str]]:
        """
        Valida se o arquivo é uma imagem válida (sem processar).

        Args:
            arquivo: Arquivo para validar

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        if arquivo.content_type not in ImageProcessor.TIPOS_PERMITIDOS:
            tipos_formatados = ", ".join([t.split("/")[1].upper() for t in ImageProcessor.TIPOS_PERMITIDOS])
            return False, f"Tipo de arquivo inválido. Use: {tipos_formatados}"

        return True, None
