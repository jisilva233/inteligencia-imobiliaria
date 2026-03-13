"""
Componente de filtros globais (sidebar)
Compartilhado por todas as páginas
"""

import streamlit as st
from utils.session_state import init_session_state, update_filtro, get_filtro
from services.bairros_service import get_cidades_list, get_bairros_por_cidade


def render_sidebar_filters() -> dict:
    """
    Renderiza a sidebar com todos os filtros globais.
    Atualiza st.session_state.filters automaticamente.

    Returns:
        dict: Dicionário com filtros atualizados
    """
    init_session_state()

    with st.sidebar:
        st.title("🔍 Filtros")

        # ====================================
        # Filtro: Cidade
        # ====================================
        cidades = get_cidades_list()

        cidade_selecionada = st.selectbox(
            label="🏙️ Cidade",
            options=[None] + cidades,
            index=0,
            format_func=lambda x: "Selecione uma cidade..." if x is None else x,
            key="filtro_cidade",
        )

        if cidade_selecionada != get_filtro("cidade_selecionada"):
            update_filtro("cidade_selecionada", cidade_selecionada)
            # Resetar bairro ao trocar cidade
            update_filtro("bairro_selecionado", None)

        # ====================================
        # Filtro: Bairro (depende da cidade)
        # ====================================
        bairros = {}
        bairro_options = [None]

        if cidade_selecionada:
            bairros = get_bairros_por_cidade(cidade_selecionada)
            bairro_options = [None] + list(bairros.values())

        bairro_selecionado = st.selectbox(
            label="🏘️ Bairro",
            options=bairro_options,
            index=0,
            format_func=lambda x: "Selecione um bairro..." if x is None else x,
            disabled=not cidade_selecionada,
            key="filtro_bairro",
        )

        if bairro_selecionado != get_filtro("bairro_selecionado"):
            update_filtro("bairro_selecionado", bairro_selecionado)

        # ====================================
        # Filtro: Faixa de Preço
        # ====================================
        st.subheader("💰 Faixa de Preço")

        preco_min = st.number_input(
            "Preço mínimo (R$)",
            value=int(get_filtro("faixa_preco_min", 0)),
            step=50000,
            format="%d",
        )

        preco_max = st.number_input(
            "Preço máximo (R$)",
            value=int(get_filtro("faixa_preco_max", 10000000)),
            step=50000,
            format="%d",
        )

        if preco_max < preco_min:
            preco_max = preco_min + 100000

        if (
            preco_min != get_filtro("faixa_preco_min")
            or preco_max != get_filtro("faixa_preco_max")
        ):
            update_filtro("faixa_preco_min", preco_min)
            update_filtro("faixa_preco_max", preco_max)

        # ====================================
        # Filtro: Score de Marketing
        # ====================================
        st.subheader("📊 Marketing")

        score_marketing_min = st.slider(
            "Score de fraqueza mínimo (0-100)",
            min_value=0,
            max_value=100,
            value=int(get_filtro("score_marketing_min", 0)),
            step=5,
        )

        if score_marketing_min != get_filtro("score_marketing_min"):
            update_filtro("score_marketing_min", score_marketing_min)

        # ====================================
        # Filtro: Status de Empreendimento
        # ====================================
        st.subheader("🏗️ Empreendimento")

        status_options = [
            "projeto",
            "fundações",
            "estrutura",
            "acabamento",
            "pronto",
        ]

        status_selecionados = st.multiselect(
            "Status de construção",
            options=status_options,
            default=get_filtro("status_empreendimento", []),
        )

        if status_selecionados != get_filtro("status_empreendimento"):
            update_filtro("status_empreendimento", status_selecionados)

        # ====================================
        # Botão: Resetar Filtros
        # ====================================
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Resetar", use_container_width=True):
                from utils.session_state import reset_filtros
                reset_filtros()
                st.rerun()

        with col2:
            st.metric("Filtros", "Ativos", label_visibility="collapsed")

    # Retornar dicionário atualizado
    return {
        "cidade_selecionada": get_filtro("cidade_selecionada"),
        "bairro_selecionado": get_filtro("bairro_selecionado"),
        "faixa_preco_min": get_filtro("faixa_preco_min"),
        "faixa_preco_max": get_filtro("faixa_preco_max"),
        "score_marketing_min": get_filtro("score_marketing_min"),
        "status_empreendimento": get_filtro("status_empreendimento"),
    }
