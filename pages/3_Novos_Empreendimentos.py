"""
Página 3: Novos Empreendimentos
Visualiza projetos em diferentes estágios de construção
"""

import streamlit as st
import pandas as pd
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from services.imoveis_service import get_imoveis_em_construcao, get_imoveis_por_empreendimento
from utils.formatters import format_currency

st.set_page_config(
    page_title="Novos Empreendimentos",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
filtros = render_sidebar_filters()

st.title("🏗️ Novos Empreendimentos")

st.markdown(
    """
    Acompanhe o pipeline de novos projetos e empreendimentos em construção,
    agrupados por estágio de desenvolvimento.
    """
)

st.markdown("---")

# Definir estágios
estágios = {
    "projeto": {"emoji": "📋", "cor": "#gray", "descricao": "Em Projeto"},
    "fundações": {"emoji": "🔨", "cor": "#orange", "descricao": "Fundações"},
    "estrutura": {"emoji": "🏗️", "cor": "#warning", "descricao": "Estrutura"},
    "acabamento": {"emoji": "🎨", "cor": "#info", "descricao": "Acabamento"},
    "pronto": {"emoji": "✅", "cor": "#success", "descricao": "Pronto"},
}

# Abas por estágio
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"{est['emoji']} {est['descricao']}"
    for est in estágios.values()
])

tabs = [tab1, tab2, tab3, tab4, tab5]
estágios_list = list(estágios.keys())

for tab, estágio in zip(tabs, estágios_list):
    with tab:
        with st.spinner(f"Carregando {estágios[estágio]['descricao']}..."):
            df_empreendimentos = get_imoveis_por_empreendimento(
                tipo_empreendimento=estágio
            )

        if df_empreendimentos.empty:
            st.info(f"Nenhum empreendimento em {estágios[estágio]['descricao']}")
        else:
            st.subheader(f"{estágios[estágio]['emoji']} {estágios[estágio]['descricao'].upper()}")

            # Mostrar como cards
            cols = st.columns(2)

            for idx, (_, row) in enumerate(df_empreendimentos.iterrows()):
                col = cols[idx % 2]

                with col:
                    with st.container(border=True):
                        st.markdown(f"**{row.get('endereco', 'N/A')[:50]}...**")
                        st.caption(f"📍 {row.get('bairro_id', 'N/A')}")

                        # Métricas
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "💰 Preço",
                                format_currency(row.get("preco", 0)),
                                label_visibility="collapsed",
                            )

                        with col2:
                            pct = row.get("percentual_conclusao", 0)
                            st.metric(
                                "🔨 Conclusão",
                                f"{pct}%" if pct > 0 else "N/A",
                                label_visibility="collapsed",
                            )

                        # Barra de progresso
                        if pct > 0:
                            st.progress(pct / 100, text=f"Progresso: {pct}%")

                        # Info adicionais
                        if row.get("area_m2"):
                            st.caption(f"📐 Área: {row.get('area_m2'):.0f}m²")

st.markdown("---")

# Stats gerais
with st.spinner("Carregando estatísticas..."):
    all_construcao = get_imoveis_em_construcao()

st.subheader("📊 Resumo Geral")

col1, col2, col3, col4, col5 = st.columns(5)

for col, estágio in zip([col1, col2, col3, col4, col5], estágios_list):
    df_estágio = get_imoveis_por_empreendimento(estágio)
    with col:
        st.metric(
            label=f"{estágios[estágio]['emoji']} {estágios[estágio]['descricao']}",
            value=len(df_estágio),
        )

st.caption("💡 Acompanhe regularmente para novas oportunidades de investimento")
