"""
Página 6: Prospecção e Pipeline de Leads
Gerencia o ciclo de vida de oportunidades de vendas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from components.tabela_exportavel import render_data_table
from services.prospeccao_service import (
    get_oportunidades_por_status,
    get_contagem_por_status,
    get_taxa_conversao,
    get_proximas_acoes,
)
from utils.formatters import format_status_badge, format_date

st.set_page_config(
    page_title="Prospecção",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
filtros = render_sidebar_filters()

st.title("🎯 Prospecção e Pipeline de Leads")

st.markdown(
    """
    Gerencie o pipeline de prospecção e acompanhe oportunidades
    em diferentes estágios do funil de vendas.

    **Estágios:**
    - 🔵 Lead Frio: Contato inicial
    - 🟡 Qualificado: Potencial confirmado
    - 🟠 Em Contato: Negociação ativa
    - 🟣 Proposta Enviada: Aguardando resposta
    - 🟢 Fechado: Venda realizada
    """
)

st.markdown("---")

# KPI: Taxa de Conversão
taxa_info = get_taxa_conversao()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total de Leads", taxa_info["total"])

with col2:
    st.metric("🟡 Qualificados", taxa_info["qualificado"])

with col3:
    st.metric("🟢 Fechados", taxa_info["fechado"])

with col4:
    st.metric("📈 Taxa Conversão", f"{taxa_info['taxa_%']:.1f}%")

st.markdown("---")

# Seletor de Status
status_opcoes = [
    "lead_frio",
    "qualificado",
    "em_contato",
    "proposta_enviada",
    "fechado",
]

status_selecionado = st.selectbox(
    "Filtrar por status",
    options=[None] + status_opcoes,
    format_func=lambda x: "Todos" if x is None else format_status_badge(x),
)

st.markdown("---")

with st.spinner("🔄 Carregando oportunidades..."):
    df_oportunidades = get_oportunidades_por_status(status=status_selecionado)

if df_oportunidades.empty:
    st.info("Nenhuma oportunidade encontrada com este filtro")
else:
    # ====== Gráfico: Distribuição por Status ======
    st.subheader("📊 Distribuição do Pipeline")

    contagem = get_contagem_por_status()

    if contagem:
        df_status = pd.DataFrame([
            {"Status": k, "Quantidade": v}
            for k, v in contagem.items()
        ])

        fig = px.pie(
            df_status,
            values="Quantidade",
            names="Status",
            title="Oportunidades por Status",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ====== Tabela de Oportunidades ======
    st.subheader("📋 Oportunidades Detalhadas")

    df_tabela = df_oportunidades[[
        "contato_nome", "contato_email", "score_qualificacao", "status", "data_deteccao"
    ]].copy()

    df_tabela.columns = ["Contato", "Email", "Score", "Status", "Data Detecção"]
    df_tabela["Status"] = df_tabela["Status"].apply(format_status_badge)

    render_data_table(
        df_tabela,
        titulo="Oportunidades",
        exportar_para=["csv", "excel"],
    )

    st.markdown("---")

    # ====== Próximas Ações ======
    st.subheader("📅 Próximas Ações (7 dias)")

    df_proximas = get_proximas_acoes(dias=7)

    if not df_proximas.empty:
        st.info(f"⏰ {len(df_proximas)} ação(ões) programada(s) para os próximos 7 dias")

        df_acao = df_proximas[[
            "contato_nome", "imobiliaria_nome", "data_proxima_acao", "status"
        ]].copy()

        df_acao.columns = ["Contato", "Imobiliária", "Data da Ação", "Status"]
        df_acao["Data da Ação"] = df_acao["Data da Ação"].apply(format_date)
        df_acao["Status"] = df_acao["Status"].apply(format_status_badge)

        render_data_table(
            df_acao,
            titulo="Ações Programadas",
        )
    else:
        st.caption("Nenhuma ação programada para os próximos 7 dias")

st.caption("💡 Acompanhe regularmente o pipeline para melhorar a taxa de conversão")
