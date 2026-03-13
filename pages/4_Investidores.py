"""
Página 4: Análise de Investidores
Identifica compradores com padrão de múltiplos investimentos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from components.tabela_exportavel import render_data_table, render_data_table_with_search
from services.investidores_service import get_top_investidores, get_imoveis_por_investidor
from utils.formatters import format_currency, format_contato

st.set_page_config(
    page_title="Investidores",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
filtros = render_sidebar_filters()

st.title("💼 Análise de Investidores")

st.markdown(
    """
    Identifique e analise os principais investidores do mercado imobiliário,
    seus padrões de compra e oportunidades de negócio.
    """
)

st.markdown("---")

limite = st.slider("Mostrar top N investidores", 5, 100, 50)

with st.spinner("🔄 Carregando investidores..."):
    df_investidores = get_top_investidores(limite=limite)

if df_investidores.empty:
    st.warning("❌ Nenhum investidor encontrado")
else:
    # ====== TOP 3 Investidores ======
    st.subheader("🏆 Top 3 Investidores")

    col1, col2, col3 = st.columns(3)

    for idx, (_, row) in enumerate(df_investidores.head(3).iterrows()):
        with [col1, col2, col3][idx]:
            with st.container(border=True):
                st.metric(
                    label=f"{['🥇', '🥈', '🥉'][idx]} {row.get('nome', 'N/A')}",
                    value=int(row.get('qtd_imoveis', 0)),
                    delta="imóveis",
                )
                st.caption(f"💰 {format_currency(row.get('valor_total_investido', 0))}")
                if row.get('bairro_preferido'):
                    st.caption(f"📍 Bairro: {row.get('bairro_preferido')}")

    st.markdown("---")

    # ====== Gráfico Dispersão ======
    st.subheader("📈 Padrão de Investimento")

    fig = px.scatter(
        df_investidores,
        x="qtd_imoveis",
        y="valor_total_investido",
        hover_name="nome",
        hover_data={"bairro_preferido": True, "tipo_propriedade_preferida": True},
        title="Valor Total vs Quantidade de Imóveis",
        labels={
            "qtd_imoveis": "Quantidade de Imóveis",
            "valor_total_investido": "Valor Total Investido (R$)",
        },
    )

    fig.update_layout(height=400, hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ====== Tabela de Investidores ======
    st.subheader("📊 Listagem de Investidores")

    df_tabela = df_investidores[[
        "nome", "email", "qtd_imoveis", "valor_total_investido", "bairro_preferido"
    ]].copy()

    df_tabela.columns = ["Nome", "Email", "# Imóveis", "Valor Total", "Bairro Preferido"]
    df_tabela["Valor Total"] = df_tabela["Valor Total"].apply(format_currency)

    render_data_table_with_search(
        df_tabela,
        titulo="Investidores",
        coluna_busca="Nome",
        exportar_para=["csv", "excel"],
    )

    st.markdown("---")

    # ====== Expandible: Imóveis por Investidor ======
    st.subheader("🏠 Imóveis por Investidor")

    investidor_selecionado = st.selectbox(
        "Selecione um investidor para ver seus imóveis",
        options=df_investidores["id"],
        format_func=lambda x: next(
            (row["nome"] for _, row in df_investidores.iterrows() if row["id"] == x),
            "N/A"
        ),
    )

    if investidor_selecionado:
        with st.spinner("Carregando imóveis..."):
            df_imoveis_inv = get_imoveis_por_investidor(investidor_selecionado)

        if not df_imoveis_inv.empty:
            df_imoveis_tabela = df_imoveis_inv[[
                "endereco", "preco", "area_m2", "quartos", "bairro_id"
            ]].copy()

            df_imoveis_tabela.columns = ["Endereço", "Preço", "Área (m²)", "Quartos", "Bairro"]
            df_imoveis_tabela["Preço"] = df_imoveis_tabela["Preço"].apply(format_currency)

            render_data_table(
                df_imoveis_tabela,
                titulo="Imóveis do Investidor",
                exportar_para=["csv"],
            )
        else:
            st.info("Nenhum imóvel associado a este investidor")

st.caption("💡 Dados de investidores ajudam a identificar tendências de mercado e oportunidades")
