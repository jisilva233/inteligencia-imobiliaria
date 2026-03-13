"""
Service para dados de imobiliárias
"""

import streamlit as st
import pandas as pd
from services.supabase_client import get_supabase_client
from config import settings


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_all_imobiliarias(cidade_id: str = None) -> pd.DataFrame:
    """
    Busca todas as imobiliárias, opcionalmente filtradas por cidade.

    Args:
        cidade_id (str): ID da cidade (UUID) ou None para todas

    Returns:
        pd.DataFrame: DataFrame com imobiliárias
    """
    try:
        client = get_supabase_client()
        query = client.table("imobiliarias").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.execute()
        df = pd.DataFrame(response.data)

        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imobiliárias: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imobiliarias_com_score(cidade_id: str = None, min_score: float = 0) -> pd.DataFrame:
    """
    Busca imobiliárias e filtra por score mínimo.

    Args:
        cidade_id (str): ID da cidade ou None
        min_score (float): Score mínimo (0-10)

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df = get_all_imobiliarias(cidade_id)

    if not df.empty and "score_oportunidade" in df.columns:
        df = df[df["score_oportunidade"] >= min_score].copy()

    return df.sort_values("score_oportunidade", ascending=False)


@st.cache_data(ttl=settings.CACHE_TTL_PROFILE)
def get_imobiliaria_por_id(imobiliaria_id: str) -> dict:
    """
    Busca dados detalhados de uma imobiliária.

    Args:
        imobiliaria_id (str): ID da imobiliária (UUID)

    Returns:
        dict: Dados da imobiliária ou dicionário vazio
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("imobiliarias")
            .select("*")
            .eq("id", imobiliaria_id)
            .single()
            .execute()
        )

        return response.data if response.data else {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar imobiliária: {str(e)}")
        return {}


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_top_imobiliarias(limite: int = 10, cidade_id: str = None) -> pd.DataFrame:
    """
    Retorna as top N imobiliárias por score.

    Args:
        limite (int): Quantidade máxima de resultados
        cidade_id (str): ID da cidade ou None

    Returns:
        pd.DataFrame: Top imobiliárias
    """
    df = get_all_imobiliarias(cidade_id)

    if not df.empty:
        df = df.sort_values("score_oportunidade", ascending=False).head(limite)

    return df


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_cidades() -> pd.DataFrame:
    """
    Busca todas as cidades cadastradas.

    Returns:
        pd.DataFrame: DataFrame com cidades
    """
    try:
        client = get_supabase_client()
        response = client.table("cidades").select("*").execute()
        df = pd.DataFrame(response.data)
        return df.sort_values("nome")
    except Exception as e:
        st.error(f"❌ Erro ao carregar cidades: {str(e)}")
        return pd.DataFrame()


def count_imobiliarias_by_cidade() -> dict:
    """
    Conta quantas imobiliárias existem por cidade.

    Returns:
        dict: Mapeamento {cidade_id: quantidade}
    """
    df = get_all_imobiliarias()

    if df.empty:
        return {}

    return dict(df.groupby("cidade_id").size())
