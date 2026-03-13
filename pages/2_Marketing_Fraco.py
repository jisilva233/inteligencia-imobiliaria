"""
Página 2: Imóveis com Marketing Fraco
Identifica oportunidades de melhoria em anúncios
"""

import streamlit as st
import pandas as pd
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from components.tabela_exportavel import render_data_table_with_search
from services.imoveis_service import get_imoveis_marketing_fraco
from utils.formatters import format_currency, format_marketing_score_badge

st.set_page_config(
    page_title="Marketing Fraco",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
filtros = render_sidebar_filters()

st.title("📸 Imóveis com Marketing Fraco")

st.markdown(
    """
    Identifique imóveis com pouca visibilidade e oportunidades de melhoria.

    **Score de Fraqueza (0-100):**
    - 0-20: ✅ Excelente (fotos, vídeos, tour virtual)
    - 21-40: ✔️ Bom
    - 41-60: ⚠️ Regular (faltam elementos)
    - 61-80: ❌ Fraco (poucos elementos)
    - 81-100: 🔴 Muito fraco (mínimos elementos)
    """
)

st.markdown("---")

# Controle de score mínimo
score_minimo = st.slider(
    "Filtrar por score mínimo de fraqueza",
    min_value=0,
    max_value=100,
    value=int(filtros.get("score_marketing_min", 40)),
    step=5,
)

st.markdown("---")

with st.spinner("🔄 Carregando imóveis..."):
    df_fraco = get_imoveis_marketing_fraco(score_minimo=score_minimo)

if df_fraco.empty:
    st.info("✅ Nenhum imóvel encontrado com marketing fraco!")
else:
    # Preparar dados
    df_exibicao = df_fraco[[
        "endereco", "preco", "bairro_nome", "qtd_fotos", "tem_video", "score_fraqueza_marketing"
    ]].copy()

    df_exibicao.columns = ["Endereço", "Preço", "Bairro", "Fotos", "Vídeo", "Score Fraqueza"]

    # Formatar preço
    df_exibicao["Preço"] = df_exibicao["Preço"].apply(format_currency)

    # Formatar vídeo
    df_exibicao["Vídeo"] = df_exibicao["Vídeo"].apply(lambda x: "✅ Sim" if x else "❌ Não")

    # Renderizar tabela
    render_data_table_with_search(
        df_exibicao,
        titulo="Imóveis com Marketing Fraco",
        coluna_busca="Endereço",
        exportar_para=["csv", "excel"],
    )

    st.markdown("---")

    # Stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📊 Total de Imóveis",
            value=len(df_fraco),
        )

    with col2:
        media_score = float(df_fraco["score_fraqueza_marketing"].mean())
        st.metric(
            label="📈 Score Médio",
            value=f"{media_score:.1f}/100",
        )

    with col3:
        sem_video = len(df_fraco[df_fraco["tem_video"] == False])
        st.metric(
            label="📹 Sem Vídeo",
            value=sem_video,
        )

st.caption("💡 Dica: Imóveis com fraco marketing têm menor visibilidade. Considere adicionar fotos, vídeos ou tours virtuais.")
