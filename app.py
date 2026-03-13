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
# CSS Customizado — Visual Moderno Dark
# ============================================
st.markdown("""
<style>
/* Fundo principal */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 50%, #0a0a1a 100%);
}

/* Header hero */
.hero-container {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #7c3aed33;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 24px;
    text-align: center;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7c3aed, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
}

/* Cards de seção */
.section-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #7c3aed44;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.section-card:hover {
    border-color: #7c3aed;
    box-shadow: 0 0 20px #7c3aed33;
}

.section-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.section-title {
    color: #a78bfa;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 8px;
}

.section-desc {
    color: #64748b;
    font-size: 0.9rem;
}

/* Métricas */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #7c3aed44;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #64748b !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0a1a 100%);
    border-right: 1px solid #7c3aed33;
}

/* Botões */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    box-shadow: 0 0 15px #7c3aed66;
    transform: translateY(-1px);
}

/* Divisores */
hr {
    border-color: #1e293b;
}

/* Alertas */
.stSuccess {
    background: #052e16;
    border: 1px solid #16a34a;
    border-radius: 8px;
}

/* Status badge */
.status-badge {
    display: inline-block;
    background: #052e16;
    color: #4ade80;
    border: 1px solid #16a34a;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Page links */
.stPageLink {
    color: #7c3aed !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# Inicialização
# ============================================
init_session_state()

# ============================================
# Validar configurações
# ============================================
config_errors = settings.validate()
missing_critical = settings.check_critical()
if missing_critical:
    st.error(f"❌ Configurações obrigatórias faltando: {', '.join(missing_critical)}")
    st.stop()

# ============================================
# Renderizar Sidebar
# ============================================
filtros = render_sidebar_filters()

# ============================================
# Hero Header
# ============================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🏠 Inteligência Imobiliária</div>
    <div class="hero-subtitle">Dashboard analítico para o mercado imobiliário brasileiro</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# Health Check
# ============================================
with st.spinner("Conectando ao banco de dados..."):
    connection_result = test_connection()

if connection_result["success"]:
    stats = connection_result["stats"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="✅ Status", value="Online")
    with col2:
        st.metric(label="🏙️ Cidades", value=stats["cidades"])
    with col3:
        st.metric(label="🏘️ Bairros", value=stats["bairros"])
    with col4:
        st.metric(label="🏠 Imóveis", value=stats["imoveis"])
else:
    st.error(connection_result["message"])
    st.stop()

st.markdown("---")

# ============================================
# Cards das Seções
# ============================================
st.markdown("### 📋 Módulos do Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">📍</div>
        <div class="section-title">Mapa de Imobiliárias</div>
        <div class="section-desc">Visualize a localização e score de todas as imobiliárias em mapa interativo.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Mapa_Imobiliarias.py", label="→ Abrir Mapa")

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">📊</div>
        <div class="section-title">Ranking de Bairros</div>
        <div class="section-desc">Score composto: 40% valorização + 35% demanda + 25% oferta.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_Ranking_Bairros.py", label="→ Ver Ranking")

with col3:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">📸</div>
        <div class="section-title">Marketing Fraco</div>
        <div class="section-desc">Identifique imóveis com pouca visibilidade e oportunidades de melhoria.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Marketing_Fraco.py", label="→ Analisar")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">🏗️</div>
        <div class="section-title">Novos Empreendimentos</div>
        <div class="section-desc">Pipeline de projetos em construção agrupados por estágio de obra.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Novos_Empreendimentos.py", label="→ Ver Projetos")

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">💼</div>
        <div class="section-title">Investidores</div>
        <div class="section-desc">Perfil de compradores com padrão de múltiplos investimentos.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Investidores.py", label="→ Explorar")

with col3:
    st.markdown("""
    <div class="section-card">
        <div class="section-icon">🎯</div>
        <div class="section-title">Prospecção</div>
        <div class="section-desc">Pipeline de leads qualificados e oportunidades de vendas.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_Prospeccao.py", label="→ Gerenciar")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #334155; font-size: 0.8rem; padding: 16px 0;">
    🔐 Dados protegidos por RLS do Supabase &nbsp;|&nbsp; v1.0.0 &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)
