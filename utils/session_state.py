"""
Gerenciamento de session state para filtros globais
Streamlit re-executa o script a cada interação, então usamos st.session_state
para persistir valores de filtros entre execuções
"""

import streamlit as st


def init_session_state():
    """
    Inicializa o namespace 'filters' em st.session_state com valores padrão.
    Deve ser chamado no início de toda página (app.py e pages/).
    """
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "cidade_selecionada": None,
            "bairro_selecionado": None,
            "faixa_preco_min": 0,
            "faixa_preco_max": 10000000,
            "score_marketing_min": 0,
            "status_empreendimento": [],  # multiselect
            "tipo_imovel": None,
        }


def get_filtros() -> dict:
    """
    Retorna o dicionário de filtros do session_state.

    Returns:
        dict: Dicionário com todos os filtros ativos
    """
    init_session_state()
    return st.session_state.filters.copy()


def update_filtro(chave: str, valor):
    """
    Atualiza um filtro específico no session_state.

    Args:
        chave (str): Nome do filtro (ex: 'cidade_selecionada')
        valor: Novo valor do filtro

    Returns:
        dict: Dicionário atualizado de filtros
    """
    init_session_state()
    st.session_state.filters[chave] = valor
    return st.session_state.filters.copy()


def reset_filtros():
    """Reseta todos os filtros para valores padrão"""
    st.session_state.filters = {
        "cidade_selecionada": None,
        "bairro_selecionado": None,
        "faixa_preco_min": 0,
        "faixa_preco_max": 10000000,
        "score_marketing_min": 0,
        "status_empreendimento": [],
        "tipo_imovel": None,
    }


def get_filtro(chave: str, default=None):
    """
    Retorna o valor de um filtro específico.

    Args:
        chave (str): Nome do filtro
        default: Valor padrão se a chave não existir

    Returns:
        Valor do filtro ou default
    """
    init_session_state()
    return st.session_state.filters.get(chave, default)


def set_filtros_from_dict(filtros_dict: dict):
    """
    Define múltiplos filtros de uma vez a partir de um dicionário.

    Args:
        filtros_dict (dict): Dicionário com pares chave-valor
    """
    init_session_state()
    st.session_state.filters.update(filtros_dict)
