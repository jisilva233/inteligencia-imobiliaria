"""
Página 5: Ranking de Bairros
Mostra ranking de bairros com score composto
(40% valorização + 35% demanda + 25% oferta)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from components.tabela_exportavel import render_data_table
from services.bairros_service import get_ranking_bairros, get_all_bairros

# ============================================
# Configuração da página
# ============================================
st.set_page_config(
    page_title="Ranking de Bairros",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Inicialização
# ============================================
init_session_state()

# ============================================
# Sidebar
# ============================================
filtros = render_sidebar_filters()

# ============================================
# Conteúdo Principal
# ============================================
st.title("📊 Ranking de Bairros")

st.markdown(
    """
    Ranking composto de bairros baseado em:
    - **40%** Valorização imobiliária
    - **35%** Demanda de mercado
    - **25%** Disponibilidade de oferta

    Score varia de 0 a 10 pontos.
    """
)

st.markdown("---")

# ============================================
# Controles
# ============================================
col1, col2 = st.columns(2)

with col1:
    limite_ranking = st.slider(
        "Mostrar top N bairros",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
    )

with col2:
    ordenar_por = st.selectbox(
        "Ordenar por",
        options=["score_composto", "score_valorizacao", "score_demanda", "score_oferta"],
        format_func=lambda x: {
            "score_composto": "Score Composto",
            "score_valorizacao": "Valorização",
            "score_demanda": "Demanda",
            "score_oferta": "Oferta",
        }.get(x, x),
    )

st.markdown("---")

# ============================================
# Buscar Dados
# ============================================
cidade_id = None
# TODO: Mapear cidade selecionada para ID

with st.spinner("🔄 Carregando ranking..."):
    df_ranking = get_ranking_bairros(cidade_id=cidade_id, limite=limite_ranking)

if df_ranking.empty:
    st.warning("❌ Nenhum bairro encontrado")
else:
    # Ordenar conforme seleção
    df_ranking = df_ranking.sort_values(ordenar_por, ascending=False)

    # ============================================
    # Top 3 Bairros (Destaque)
    # ============================================
    st.subheader("🏆 Top 3 Bairros")

    col1, col2, col3 = st.columns(3)

    for idx, (i, row) in enumerate(df_ranking.head(3).iterrows()):
        with [col1, col2, col3][idx]:
            with st.container(border=True):
                st.metric(
                    label=f"{['🥇', '🥈', '🥉'][idx]} {row.get('bairro_nome', 'N/A')}",
                    value=f"{row.get('score_composto', 0):.2f}/10",
                )
                st.caption(
                    f"📍 {row.get('cidade_nome', 'N/A')}"
                )
                st.caption(
                    f"🏠 {int(row.get('total_imoveis', 0))} imóveis"
                )

    st.markdown("---")

    # ============================================
    # Gráfico de Barras
    # ============================================
    st.subheader("📈 Score Composto por Bairro")

    # Preparar dados para gráfico
    df_grafico = df_ranking.head(limite_ranking).copy()
    df_grafico["label"] = df_grafico["bairro_nome"] + " (" + df_grafico["cidade_nome"] + ")"

    fig = px.bar(
        df_grafico,
        x="score_composto",
        y="label",
        orientation="h",
        color="score_composto",
        color_continuous_scale="RdYlGn",
        title="Score Composto dos Bairros",
        labels={
            "score_composto": "Score (0-10)",
            "label": "Bairro",
        },
        hover_data={
            "score_valorizacao": ":.2f",
            "score_demanda": ":.2f",
            "score_oferta": ":.2f",
            "total_imoveis": True,
            "preco_medio": ":.2f",
        },
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        hovermode="y unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ============================================
    # Tabela Detalhada
    # ============================================
    st.subheader("📊 Tabela Detalhada")

    # Formatar coluna de bairro
    df_tabela = df_ranking[
        ["bairro_nome", "cidade_nome", "score_composto", "score_valorizacao", "score_demanda", "score_oferta", "total_imoveis"]
    ].copy()

    df_tabela.columns = ["Bairro", "Cidade", "Score Total", "Valorização", "Demanda", "Oferta", "# Imóveis"]

    render_data_table(
        df_tabela,
        titulo="Ranking Completo",
        exportar_para=["csv", "excel"],
    )

    st.markdown("---")

    # ============================================
    # Análise por Dimensão
    # ============================================
    st.subheader("🔬 Análise por Dimensão")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📈 Top Valorização")
        top_val = df_ranking.nlargest(5, "score_valorizacao")[["bairro_nome", "score_valorizacao"]]
        for i, row in top_val.iterrows():
            st.caption(f"⭐ {row['bairro_nome']}: {row['score_valorizacao']:.1f}")

    with col2:
        st.markdown("#### 👥 Top Demanda")
        top_dem = df_ranking.nlargest(5, "score_demanda")[["bairro_nome", "score_demanda"]]
        for i, row in top_dem.iterrows():
            st.caption(f"⭐ {row['bairro_nome']}: {row['score_demanda']:.1f}")

    with col3:
        st.markdown("#### 📦 Top Oferta")
        top_oferta = df_ranking.nlargest(5, "score_oferta")[["bairro_nome", "score_oferta"]]
        for i, row in top_oferta.iterrows():
            st.caption(f"⭐ {row['bairro_nome']}: {row['score_oferta']:.1f}")

st.markdown("---")

st.caption("💡 Os scores são recalculados diariamente baseado em dados de mercado")
