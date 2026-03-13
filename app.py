"""
Dashboard de Inteligência Imobiliária
Página principal (Home)
"""

import streamlit as st
from utils.session_state import init_session_state
from components.filtros_globais import render_sidebar_filters
from services.supabase_client import test_connection
from config import settings

# ============================================
# Configuração da página
# ============================================
st.set_page_config(
    page_title="Inteligência Imobiliária",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Inicialização
# ============================================
init_session_state()

# ============================================
# Validar configurações
# ============================================
config_errors = settings.validate()
if config_errors:
    st.warning("⚠️ Avisos de configuração:")
    for error in config_errors:
        st.caption(error)

# ============================================
# Renderizar Sidebar
# ============================================
filtros = render_sidebar_filters()

# ============================================
# Conteúdo Principal
# ============================================
st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:
    st.title("🏠 Dashboard de Inteligência Imobiliária")

with col2:
    st.image(
        "https://via.placeholder.com/100?text=Logo",
        width=100,
    )

st.markdown(
    """
    Bem-vindo ao **Dashboard de Inteligência Imobiliária**!

    Este dashboard fornece análises avançadas do mercado imobiliário, incluindo:
    - 📍 Mapa interativo de imobiliárias
    - 📊 Ranking de bairros por valorização
    - 📸 Detecção de imóveis com marketing fraco
    - 🏗️ Pipeline de novos empreendimentos
    - 💼 Análise de investidores
    - 🎯 Prospecção de leads qualificados
    """
)

st.markdown("---")

# ============================================
# Health Check
# ============================================
st.subheader("🔍 Status do Banco de Dados")

with st.spinner("Conectando ao Supabase..."):
    connection_result = test_connection()

if connection_result["success"]:
    st.success(connection_result["message"])

    stats = connection_result["stats"]
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🏙️ Cidades",
            value=stats["cidades"],
        )

    with col2:
        st.metric(
            label="🏘️ Bairros",
            value=stats["bairros"],
        )

    with col3:
        st.metric(
            label="🏠 Imóveis",
            value=stats["imoveis"],
        )

else:
    st.error(connection_result["message"])
    st.stop()

st.markdown("---")

# ============================================
# Seções do Dashboard
# ============================================
st.subheader("📋 Seções Disponíveis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    #### 📍 Mapa de Imobiliárias
    Visualize a localização de todas as imobiliárias
    em um mapa interativo com Mapbox.
    """
    )
    st.page_link("pages/1_Mapa_Imobiliarias.py", label="Ir para Mapa →")

with col2:
    st.markdown(
        """
    #### 📊 Ranking de Bairros
    Veja os melhores bairros por score composto
    (valorização + demanda + oferta).
    """
    )
    st.page_link("pages/5_Ranking_Bairros.py", label="Ver Ranking →")

with col3:
    st.markdown(
        """
    #### 📸 Marketing Fraco
    Identifique imóveis com pouca visibilidade
    e oportunidades de melhoria.
    """
    )
    st.page_link("pages/2_Marketing_Fraco.py", label="Analisar →")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    #### 🏗️ Novos Empreendimentos
    Acompanhe o pipeline de novos projetos
    e empreendimentos em construção.
    """
    )
    st.page_link("pages/3_Novos_Empreendimentos.py", label="Ver Projetos →")

with col2:
    st.markdown(
        """
    #### 💼 Investidores
    Analise o perfil de compradores que fazem
    múltiplos investimentos.
    """
    )
    st.page_link("pages/4_Investidores.py", label="Explorar →")

with col3:
    st.markdown(
        """
    #### 🎯 Prospecção
    Gerencie o pipeline de leads qualificados
    e oportunidades de vendas.
    """
    )
    st.page_link("pages/6_Prospeccao.py", label="Gerenciar →")

st.markdown("---")

# ============================================
# Informações Gerais
# ============================================
st.subheader("ℹ️ Sobre")

st.markdown(
    """
    **Versão:** 1.0.0
    **Stack:** Python + Streamlit | Supabase | Mapbox
    **Última atualização:** 2026-03-12

    Este dashboard foi desenvolvido com o Synkra AIOS Framework
    para análise inteligente do mercado imobiliário.
    """
)

# Footer
st.divider()
st.caption("🔐 Todos os dados são privados e seguem RLS do Supabase")
