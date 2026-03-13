"""
Service para pipeline de prospecção
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from services.supabase_client import get_supabase_client
from config import settings


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_oportunidades_por_status(
    status: str = None, cidade_id: str = None
) -> pd.DataFrame:
    """
    Busca oportunidades filtradas por status.

    Args:
        status (str): Status da oportunidade:
                     'lead_frio', 'qualificado', 'em_contato', 'proposta_enviada', 'fechado'
        cidade_id (str): ID da cidade (UUID) ou None

    Returns:
        pd.DataFrame: DataFrame com oportunidades
    """
    try:
        client = get_supabase_client()

        # Usar view vw_oportunidades_qualificadas
        query = client.table("vw_oportunidades_qualificadas").select("*")

        if status:
            query = query.eq("status", status)

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.order("score_qualificacao", desc=True).execute()

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar oportunidades: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_oportunidades_todas() -> pd.DataFrame:
    """
    Busca todas as oportunidades sem filtro.

    Returns:
        pd.DataFrame: DataFrame com todas as oportunidades
    """
    return get_oportunidades_por_status()


@st.cache_data(ttl=settings.CACHE_TTL_PROFILE)
def get_oportunidade_por_id(oportunidade_id: str) -> dict:
    """
    Busca dados detalhados de uma oportunidade.

    Args:
        oportunidade_id (str): ID da oportunidade (UUID)

    Returns:
        dict: Dados da oportunidade
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("oportunidades_prospeccao")
            .select("*")
            .eq("id", oportunidade_id)
            .single()
            .execute()
        )

        return response.data if response.data else {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar oportunidade: {str(e)}")
        return {}


def update_oportunidade_status(oportunidade_id: str, novo_status: str) -> bool:
    """
    Atualiza o status de uma oportunidade.

    Args:
        oportunidade_id (str): ID da oportunidade
        novo_status (str): Novo status

    Returns:
        bool: True se sucesso, False caso contrário
    """
    try:
        client = get_supabase_client()

        response = (
            client.table("oportunidades_prospeccao")
            .update({
                "status": novo_status,
                "updated_at": datetime.now().isoformat()
            })
            .eq("id", oportunidade_id)
            .execute()
        )

        # Invalidar cache
        st.cache_data.clear()

        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar oportunidade: {str(e)}")
        return False


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_oportunidades_por_imobiliaria(imobiliaria_id: str) -> pd.DataFrame:
    """
    Busca todas as oportunidades de uma imobiliária.

    Args:
        imobiliaria_id (str): ID da imobiliária

    Returns:
        pd.DataFrame: DataFrame com oportunidades
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("oportunidades_prospeccao")
            .select("*")
            .eq("imobiliaria_id", imobiliaria_id)
            .order("score_qualificacao", desc=True)
            .execute()
        )

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar oportunidades: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_contagem_por_status(cidade_id: str = None) -> dict:
    """
    Retorna contagem de oportunidades por status.

    Args:
        cidade_id (str): ID da cidade ou None

    Returns:
        dict: {status: quantidade}
    """
    df = get_oportunidades_todas()

    if not df.empty and cidade_id:
        df = df[df["cidade_id"] == cidade_id]

    if df.empty:
        return {}

    return dict(df["status"].value_counts())


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_proximas_acoes(dias: int = 7) -> pd.DataFrame:
    """
    Busca oportunidades com ações previstas para os próximos N dias.

    Args:
        dias (int): Número de dias a frente

    Returns:
        pd.DataFrame: DataFrame com oportunidades urgentes
    """
    df = get_oportunidades_todas()

    if df.empty or "data_proxima_acao" not in df.columns:
        return pd.DataFrame()

    # Filtrar por data_proxima_acao
    try:
        df["data_proxima_acao"] = pd.to_datetime(
            df["data_proxima_acao"], errors="coerce"
        )

        hoje = pd.Timestamp.now()
        proximos_dias = hoje + pd.Timedelta(days=dias)

        df_filtrado = df[
            (df["data_proxima_acao"] >= hoje) &
            (df["data_proxima_acao"] <= proximos_dias)
        ]

        return df_filtrado.sort_values("data_proxima_acao")
    except Exception as e:
        st.error(f"❌ Erro ao filtrar próximas ações: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_taxa_conversao() -> dict:
    """
    Calcula taxa de conversão do pipeline.

    Returns:
        dict: {'total': int, 'qualificado': int, 'fechado': int, 'taxa_%': float}
    """
    df = get_oportunidades_todas()

    if df.empty:
        return {"total": 0, "qualificado": 0, "fechado": 0, "taxa_%": 0.0}

    total = len(df)
    qualificado = len(df[df["status"] == "qualificado"])
    fechado = len(df[df["status"] == "fechado"])

    taxa = (fechado / total * 100) if total > 0 else 0

    return {
        "total": total,
        "qualificado": qualificado,
        "fechado": fechado,
        "taxa_%": round(taxa, 2),
    }
