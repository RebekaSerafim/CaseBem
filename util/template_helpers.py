"""
Helpers para templates que incluem automaticamente mensagens flash
"""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from util.flash_messages import get_flashed_messages
from util.avatar_util import obter_avatar_ou_padrao, obter_caminho_avatar, avatar_existe
from util.item_foto_util import obter_foto_item_ou_padrao, obter_caminho_foto_item, foto_item_existe


def formatar_moeda(valor):
    """
    Formata um valor numérico para o padrão monetário brasileiro (R$ 1.234,56)

    Args:
        valor: Valor numérico (float, int ou string) para formatação

    Returns:
        String formatada no padrão brasileiro ou valor original se inválido
    """
    if valor is None:
        return "R$ 0,00"

    try:
        # Converte para float se necessário
        if isinstance(valor, str):
            # Remove caracteres não numéricos exceto ponto e vírgula
            valor_limpo = valor.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            valor = float(valor_limpo)
        elif isinstance(valor, int):
            valor = float(valor)

        # Formatação manual para o padrão brasileiro
        valor_str = f"{valor:.2f}"
        partes = valor_str.split('.')
        inteira = partes[0]
        decimal = partes[1]

        # Adiciona pontos a cada 3 dígitos na parte inteira
        if len(inteira) > 3:
            inteira_formatada = ""
            for i, digito in enumerate(reversed(inteira)):
                if i > 0 and i % 3 == 0:
                    inteira_formatada = "." + inteira_formatada
                inteira_formatada = digito + inteira_formatada
        else:
            inteira_formatada = inteira

        return f"R$ {inteira_formatada},{decimal}"

    except (ValueError, TypeError, AttributeError):
        return str(valor) if valor else "R$ 0,00"


def get_active_page_from_url(request: Request) -> str:
    """
    Determina qual página está ativa baseada na URL para qualquer módulo
    """
    url_path = str(request.url.path)

    # Páginas públicas
    if url_path == "/":
        return "home"
    elif url_path == "/sobre":
        return "sobre"
    elif url_path == "/contato":
        return "contato"
    elif url_path.startswith("/itens"):
        tipo_param = request.query_params.get("tipo")
        if tipo_param == "servico":
            return "servicos"
        elif tipo_param == "espaco":
            return "espacos"
        elif tipo_param == "produto":
            return "produtos"
        else:
            return "itens"
    elif url_path.startswith("/item/"):
        return "itens"

    # Páginas admin
    elif url_path == "/admin/dashboard":
        return "dashboard"
    elif url_path == "/admin/perfil":
        return "perfil"
    elif url_path.startswith("/admin/usuarios"):
        return "usuarios"
    elif url_path.startswith("/admin/categorias"):
        return "categorias"
    elif url_path.startswith("/admin/itens"):
        return "itens"
    elif url_path.startswith("/admin/relatorios"):
        return "relatorios"

    # Páginas fornecedor
    elif url_path == "/fornecedor/dashboard":
        return "dashboard"
    elif url_path == "/fornecedor/perfil":
        return "perfil"
    elif url_path.startswith("/fornecedor/itens"):
        return "itens"
    elif url_path.startswith("/fornecedor/demandas"):
        return "demandas"
    elif url_path.startswith("/fornecedor/orcamentos"):
        return "orcamentos"

    # Páginas noivo
    elif url_path == "/noivo/dashboard":
        return "dashboard"
    elif url_path == "/noivo/perfil":
        return "perfil"
    elif url_path.startswith("/noivo/fornecedores"):
        return "fornecedores"
    elif url_path.startswith("/noivo/demandas"):
        return "demandas"
    elif url_path.startswith("/noivo/orcamentos"):
        return "orcamentos"
    elif url_path.startswith("/noivo/checklist"):
        return "checklist"
    elif url_path.startswith("/noivo/favoritos"):
        return "favoritos"

    else:
        return ""

def template_response_with_flash(templates: Jinja2Templates, template_name: str, context: dict):
    """
    Cria uma TemplateResponse que inclui automaticamente mensagens flash e active_page

    Args:
        templates: Instância do Jinja2Templates
        template_name: Nome do template
        context: Contexto do template

    Returns:
        TemplateResponse com mensagens flash e active_page incluídas
    """
    if "request" in context:
        # Adicionar mensagens flash ao contexto
        flash_messages = get_flashed_messages(context["request"])
        context["flash_messages"] = flash_messages

        # Adicionar active_page ao contexto se não estiver presente
        if "active_page" not in context:
            context["active_page"] = get_active_page_from_url(context["request"])

    return templates.TemplateResponse(template_name, context)


def formatar_data(data):
    """
    Formata uma data do formato ISO (yyyy-mm-dd) para o padrão brasileiro (dd/mm/yyyy)

    Args:
        data: Data no formato string (yyyy-mm-dd) ou objeto date/datetime

    Returns:
        String formatada no padrão brasileiro ou string original se inválida
    """
    if data is None:
        return "Data não disponível"

    try:
        from datetime import datetime, date

        # Se já é um objeto date ou datetime
        if isinstance(data, datetime):
            return data.strftime("%d/%m/%Y")
        elif isinstance(data, date):
            return data.strftime("%d/%m/%Y")

        # Se é string, tenta converter
        if isinstance(data, str):
            data = data.strip()
            if not data:
                return "Data não disponível"

            # Tenta formato yyyy-mm-dd
            try:
                data_obj = datetime.strptime(data, "%Y-%m-%d")
                return data_obj.strftime("%d/%m/%Y")
            except ValueError:
                pass

            # Tenta formato yyyy-mm-dd hh:mm:ss
            try:
                data_obj = datetime.strptime(data[:10], "%Y-%m-%d")
                return data_obj.strftime("%d/%m/%Y")
            except ValueError:
                pass

        return str(data)
    except (ValueError, TypeError, AttributeError):
        return str(data) if data else "Data não disponível"


def formatar_data_hora(data_hora):
    """
    Formata uma data/hora do formato ISO (yyyy-mm-dd hh:mm:ss) para o padrão brasileiro (dd/mm/yyyy às hh:mm)

    Args:
        data_hora: Data/hora no formato string ISO ou objeto datetime

    Returns:
        String formatada no padrão brasileiro ou string original se inválida
    """
    if data_hora is None:
        return "Data não disponível"

    try:
        from datetime import datetime, date

        # Se já é um objeto datetime
        if isinstance(data_hora, datetime):
            return data_hora.strftime("%d/%m/%Y às %H:%M")
        elif isinstance(data_hora, date):
            return data_hora.strftime("%d/%m/%Y")

        # Se é string, tenta converter
        if isinstance(data_hora, str):
            data_hora = data_hora.strip()
            if not data_hora:
                return "Data não disponível"

            # Tenta formato yyyy-mm-dd hh:mm:ss
            try:
                data_obj = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
                return data_obj.strftime("%d/%m/%Y às %H:%M")
            except ValueError:
                pass

            # Tenta formato yyyy-mm-dd
            try:
                data_obj = datetime.strptime(data_hora, "%Y-%m-%d")
                return data_obj.strftime("%d/%m/%Y")
            except ValueError:
                pass

            # Se contém 'T' (formato ISO com T)
            if 'T' in data_hora:
                try:
                    data_obj = datetime.fromisoformat(data_hora.replace('Z', '+00:00'))
                    return data_obj.strftime("%d/%m/%Y às %H:%M")
                except ValueError:
                    pass

        return str(data_hora)
    except (ValueError, TypeError, AttributeError):
        return str(data_hora) if data_hora else "Data não disponível"


def configurar_filtros_jinja(templates: Jinja2Templates):
    """
    Configura filtros customizados para os templates Jinja2

    Args:
        templates: Instância do Jinja2Templates para adicionar os filtros
    """
    templates.env.filters['moeda'] = formatar_moeda
    templates.env.filters['formatar_data'] = formatar_data
    templates.env.filters['formatar_data_hora'] = formatar_data_hora
    templates.env.globals['obter_avatar_ou_padrao'] = obter_avatar_ou_padrao
    templates.env.globals['obter_caminho_avatar'] = obter_caminho_avatar
    templates.env.globals['avatar_existe'] = avatar_existe
    templates.env.globals['obter_foto_item_ou_padrao'] = obter_foto_item_ou_padrao
    templates.env.globals['obter_caminho_foto_item'] = obter_caminho_foto_item
    templates.env.globals['foto_item_existe'] = foto_item_existe
    templates.env.globals['get_active_page_from_url'] = get_active_page_from_url