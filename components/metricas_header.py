"""
Componente de header com KPIs principais
"""

import streamlit as st
import pandas as pd
from utils.formatters import format_currency
from services.imoveis_service import (
    get_imoveis_com_filtros,
    get_imoveis_marketing_fraco,
    count_imoveis_total,
    get_preco_medio_imoveis,
)
from services.imobiliarias_service import get_all_imobiliarias
from services.bairros_service import get_all_bairros


def render_metrics_header(filtros: dict):
    """
    Renderiza header com métricas principais.

    Args:
        filtros (dict): Dicionário com filtros globais
    """
    st.markdown("---")

    # Buscar dados baseado em filtros
    cidade_id = None
    bairro_id = None

    # TODO: Mapear nomes para IDs
    # Por enquanto, usar dados globais

    # Buscar dados
    df_imoveis = get_imoveis_com_filtros(
        cidade_id=cidade_id,
        bairro_id=bairro_id,
        preco_min=filtros.get("faixa_preco_min", 0),
        preco_max=filtros.get("faixa_preco_max", 10000000),
    )

    df_marketing_fraco = get_imoveis_marketing_fraco(
        score_minimo=filtros.get("score_marketing_min", 0),
        cidade_id=cidade_id,
    )

    df_imobiliarias = get_all_imobiliarias(cidade_id=cidade_id)
    df_bairros = get_all_bairros(cidade_id=cidade_id)

    # Calcular métricas
    total_imoveis = len(df_imoveis) if not df_imoveis.empty else 0
    total_imobiliarias = len(df_imobiliarias) if not df_imobiliarias.empty else 0
    total_bairros = len(df_bairros) if not df_bairros.empty else 0

    preco_medio = (
        float(df_imoveis["preco"].mean())
        if not df_imoveis.empty and "preco" in df_imoveis.columns
        else 0.0
    )

    marketing_fraco_count = len(df_marketing_fraco) if not df_marketing_fraco.empty else 0

    # Renderizar em colunas
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="🏠 Imóveis",
            value=total_imoveis,
            delta=None,
        )

    with col2:
        st.metric(
            label="🏢 Imobiliárias",
            value=total_imobiliarias,
            delta=None,
        )

    with col3:
        st.metric(
            label="🏘️ Bairros",
            value=total_bairros,
            delta=None,
        )

    with col4:
        st.metric(
            label="💰 Preço Médio",
            value=format_currency(preco_medio),
            delta=None,
        )

    with col5:
        st.metric(
            label="⚠️ Marketing Fraco",
            value=marketing_fraco_count,
            delta=None,
        )

    st.markdown("---")
