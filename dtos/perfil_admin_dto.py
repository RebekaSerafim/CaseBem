from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class PerfilAdminDTO(BaseModel):
    """DTO para dados do formulário de perfil do administrador"""

    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do administrador")
    email: EmailStr = Field(..., description="E-mail do administrador")
    telefone: Optional[str] = Field(None, description="Telefone do administrador")
    cargo: Optional[str] = Field(None, max_length=50, description="Cargo do administrador")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=50, description="Cidade")
    estado: Optional[str] = Field(None, max_length=2, description="Estado (sigla UF)")
    observacoes: Optional[str] = Field(None, max_length=1000, description="Observações sobre o administrador")

    @validator('nome')
    def validar_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome é obrigatório')

        # Remover espaços extras
        nome = ' '.join(v.split())

        if len(nome) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')

        if len(nome) > 100:
            raise ValueError('Nome deve ter no máximo 100 caracteres')

        # Verificar se contém apenas letras, espaços e acentos
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            raise ValueError('Nome deve conter apenas letras e espaços')

        return nome

    @validator('telefone')
    def validar_telefone(cls, v):
        if not v:
            return v

        # Remover caracteres especiais
        telefone = re.sub(r'[^0-9]', '', v)

        if len(telefone) < 10 or len(telefone) > 11:
            raise ValueError('Telefone deve ter 10 ou 11 dígitos')

        # Validar DDD
        ddd = telefone[:2]
        if not (11 <= int(ddd) <= 99):
            raise ValueError('DDD inválido')

        return telefone

    @validator('cargo')
    def validar_cargo(cls, v):
        if v is not None:
            # Remover espaços extras
            cargo = ' '.join(v.split()) if v.strip() else None

            if cargo and len(cargo) > 50:
                raise ValueError('Cargo deve ter no máximo 50 caracteres')

            return cargo
        return v

    @validator('endereco')
    def validar_endereco(cls, v):
        if v is not None:
            # Remover espaços extras
            endereco = ' '.join(v.split()) if v.strip() else None

            if endereco and len(endereco) > 200:
                raise ValueError('Endereço deve ter no máximo 200 caracteres')

            return endereco
        return v

    @validator('cidade')
    def validar_cidade(cls, v):
        if v is not None:
            # Remover espaços extras
            cidade = ' '.join(v.split()) if v.strip() else None

            if cidade:
                if len(cidade) > 50:
                    raise ValueError('Cidade deve ter no máximo 50 caracteres')

                # Verificar se contém apenas letras, espaços e acentos
                if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', cidade):
                    raise ValueError('Cidade deve conter apenas letras e espaços')

            return cidade
        return v

    @validator('estado')
    def validar_estado(cls, v):
        if v is not None:
            estado = v.strip().upper()

            if estado:
                if len(estado) != 2:
                    raise ValueError('Estado deve ter exatamente 2 caracteres (sigla UF)')

                # Lista de estados brasileiros válidos
                estados_validos = [
                    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                    'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                    'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
                ]

                if estado not in estados_validos:
                    raise ValueError('Sigla de estado inválida')

            return estado
        return v

    @validator('observacoes')
    def validar_observacoes(cls, v):
        if v is not None:
            # Remover espaços extras
            observacoes = ' '.join(v.split()) if v.strip() else None

            if observacoes and len(observacoes) > 1000:
                raise ValueError('Observações devem ter no máximo 1000 caracteres')

            return observacoes
        return v

    class Config:
        str_strip_whitespace = True
        validate_assignment = True
        schema_extra = {
            "example": {
                "nome": "Maria Silva",
                "email": "maria.admin@casebem.com",
                "telefone": "(11) 99999-9999",
                "cargo": "Gerente de Sistemas",
                "endereco": "Rua das Flores, 123 - Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "observacoes": "Responsável pela administração geral do sistema"
            }
        }