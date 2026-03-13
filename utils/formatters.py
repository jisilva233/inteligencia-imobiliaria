"""
Funções de formatação para exibição de dados
"""

from datetime import datetime, date
import locale

# Tentar configurar locale para português
try:
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
except:
    pass


def format_currency(valor: float, simbolo: str = "R$") -> str:
    """
    Formata valor numérico como moeda.

    Args:
        valor (float): Valor a formatar
        simbolo (str): Símbolo monetário (padrão: R$)

    Returns:
        str: Valor formatado (ex: "R$ 1.234.567,89")
    """
    if valor is None:
        return "N/A"

    try:
        # Formato: R$ 1.234.567,89
        return f"{simbolo} {valor:,.2f}".replace(",", "|").replace(".", ",").replace("|", ".")
    except:
        return f"{simbolo} {valor}"


def format_percentage(valor: float, casas_decimais: int = 2) -> str:
    """
    Formata valor como percentual.

    Args:
        valor (float): Valor entre 0 e 100
        casas_decimais (int): Casas decimais a exibir

    Returns:
        str: Valor formatado (ex: "45,50%")
    """
    if valor is None:
        return "N/A"

    try:
        formato = f"{{:.{casas_decimais}f}}%".format(valor)
        return formato.replace(".", ",")
    except:
        return f"{valor}%"


def format_date(data: date) -> str:
    """
    Formata data em formato brasileiro.

    Args:
        data (date): Data a formatar

    Returns:
        str: Data formatada (ex: "31/12/2025")
    """
    if data is None:
        return "N/A"

    try:
        if isinstance(data, str):
            data = datetime.fromisoformat(data).date()

        return data.strftime("%d/%m/%Y")
    except:
        return str(data)


def format_area(area_m2: float) -> str:
    """
    Formata área em metros quadrados.

    Args:
        area_m2 (float): Área em m²

    Returns:
        str: Área formatada (ex: "150,50 m²")
    """
    if area_m2 is None:
        return "N/A"

    try:
        return f"{area_m2:,.2f} m²".replace(",", "|").replace(".", ",").replace("|", ".")
    except:
        return f"{area_m2} m²"


def format_score(score: float, max_score: int = 10) -> str:
    """
    Formata score numérico com estrelas ou barra.

    Args:
        score (float): Valor do score
        max_score (int): Valor máximo do score

    Returns:
        str: Score formatado com emoji (ex: "7.5/10 ⭐⭐⭐⭐⭐⭐⭐")
    """
    if score is None:
        return "N/A"

    try:
        stars = int(score * 5 / max_score)  # Converter para 0-5 estrelas
        stars = max(0, min(5, stars))  # Limitar entre 0 e 5

        formatted_score = f"{score:.1f}/{max_score}"
        stars_visual = "⭐" * stars + "☆" * (5 - stars)

        return f"{formatted_score} {stars_visual}"
    except:
        return f"{score}/{max_score}"


def format_bairro_name(nome: str) -> str:
    """
    Formata nome de bairro com capitalização correta.

    Args:
        nome (str): Nome do bairro

    Returns:
        str: Nome capitalizado
    """
    if not nome:
        return "N/A"

    return nome.title()


def format_cidade_full(cidade: str, estado: str) -> str:
    """
    Formata nome completo de cidade com estado.

    Args:
        cidade (str): Nome da cidade
        estado (str): Sigla do estado (ex: "SP", "RJ")

    Returns:
        str: Formato "São Paulo, SP"
    """
    if not cidade:
        return "N/A"

    return f"{cidade}, {estado}" if estado else cidade


def format_contato(email: str = None, telefone: str = None) -> str:
    """
    Formata informações de contato.

    Args:
        email (str): Email
        telefone (str): Telefone

    Returns:
        str: Contato formatado
    """
    parts = []

    if email:
        parts.append(f"📧 {email}")

    if telefone:
        parts.append(f"📞 {telefone}")

    return " | ".join(parts) if parts else "Sem contato"


def format_marketing_score_badge(score: float) -> str:
    """
    Retorna emoji/badge baseado em score de marketing fraco.
    0-20: ✅ Excelente
    21-40: ✔️ Bom
    41-60: ⚠️ Regular
    61-80: ❌ Fraco
    81-100: 🔴 Muito fraco

    Args:
        score (float): Score de fraqueza de marketing (0-100)

    Returns:
        str: Badge com emoji
    """
    if score is None:
        return "❓"

    if score <= 20:
        return "✅ Excelente"
    elif score <= 40:
        return "✔️ Bom"
    elif score <= 60:
        return "⚠️ Regular"
    elif score <= 80:
        return "❌ Fraco"
    else:
        return "🔴 Muito fraco"


def format_status_badge(status: str) -> str:
    """
    Retorna emoji/badge para status de oportunidade.

    Args:
        status (str): Status da oportunidade

    Returns:
        str: Status formatado com emoji
    """
    badges = {
        "lead_frio": "🔵 Lead Frio",
        "qualificado": "🟡 Qualificado",
        "em_contato": "🟠 Em Contato",
        "proposta_enviada": "🟣 Proposta Enviada",
        "fechado": "🟢 Fechado",
    }
    return badges.get(status, status)
