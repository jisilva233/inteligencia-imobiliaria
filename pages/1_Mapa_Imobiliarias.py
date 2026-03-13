"""
Página 1: Mapa Interativo de Imobiliárias
Mostra localização de todas as imobiliárias em mapa Mapbox via pydeck
"""

import streamlit as st
import pandas as pd
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from services.imobiliarias_service import get_all_imobiliarias, get_cidades
from utils.map_helpers import (
    create_mapbox_layer,
    create_map_with_layer,
    get_city_center,
    format_map_data,
)

# ============================================
# Configuração da página
# ============================================
st.set_page_config(
    page_title="Mapa de Imobiliárias",
    page_icon="📍",
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
st.title("📍 Mapa de Imobiliárias")

st.markdown(
    """
    Visualize todas as imobiliárias cadastradas em um mapa interativo.

    - 🟢 **Verde**: Score de oportunidade alto (8-10)
    - 🟡 **Amarelo**: Score médio (5-8)
    - 🔴 **Vermelho**: Score baixo (0-5)

    O tamanho do ponto é proporcional ao score.
    """
)

st.markdown("---")

# ============================================
# Buscar Dados
# ============================================
# Tentar mapear cidade selecionada para ID
cidade_id = None
if filtros.get("cidade_selecionada"):
    # TODO: Melhorar mapeamento de cidade para ID
    # Por enquanto, buscar todas as imobiliárias
    pass

with st.spinner("🔄 Carregando dados..."):
    df_imobiliarias = get_all_imobiliarias(cidade_id=cidade_id)

# ============================================
# Processar dados
# ============================================
if df_imobiliarias.empty:
    st.warning("❌ Nenhuma imobiliária encontrada")
else:
    # Formatar dados para mapa
    df_mapa = format_map_data(df_imobiliarias)

    # Criar layer
    layer = create_mapbox_layer(
        df=df_mapa,
        latitude_col="latitude",
        longitude_col="longitude",
        color_col="score_oportunidade",
        size_col="score_oportunidade",
        label_col="nome",
    )

    # Criar mapa
    mapa = create_map_with_layer(
        df=df_mapa,
        layer=layer,
        cidade=filtros.get("cidade_selecionada"),
        title="Imobiliárias",
    )

    # Renderizar mapa
    st.pydeck_chart(mapa)

st.markdown("---")

# ============================================
# Tabela de Imobiliárias
# ============================================
st.subheader("📊 Dados das Imobiliárias")

if not df_imobiliarias.empty:
    # Selecionar colunas relevantes
    colunas_exibicao = ["nome", "latitude", "longitude", "score_oportunidade", "qtd_imoveis_anunciados"]
    df_exibicao = df_imobiliarias[[col for col in colunas_exibicao if col in df_imobiliarias.columns]].copy()

    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True,
    )

    # Stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📍 Total de Imobiliárias",
            value=len(df_imobiliarias),
        )

    with col2:
        score_medio = float(df_imobiliarias["score_oportunidade"].mean()) if "score_oportunidade" in df_imobiliarias.columns else 0
        st.metric(
            label="⭐ Score Médio",
            value=f"{score_medio:.1f}/10",
        )

    with col3:
        qtd_media = int(df_imobiliarias["qtd_imoveis_anunciados"].mean()) if "qtd_imoveis_anunciados" in df_imobiliarias.columns else 0
        st.metric(
            label="🏠 Imóveis Médio",
            value=qtd_media,
        )
else:
    st.info("Nenhuma imobiliária encontrada com os filtros selecionados")

st.markdown("---")

# Footer
st.caption("💡 Dica: Clique nos pontos do mapa para obter mais informações")
