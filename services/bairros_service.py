"""
Service para dados de bairros e ranking
"""

import streamlit as st
import pandas as pd
from services.supabase_client import get_supabase_client
from config import settings


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_all_bairros(cidade_id: str = None) -> pd.DataFrame:
    """
    Busca todos os bairros, opcionalmente filtrados por cidade.

    Args:
        cidade_id (str): ID da cidade (UUID) ou None

    Returns:
        pd.DataFrame: DataFrame com bairros
    """
    try:
        client = get_supabase_client()
        query = client.table("bairros").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.execute()
        df = pd.DataFrame(response.data)
        return df.sort_values("nome")
    except Exception as e:
        st.error(f"❌ Erro ao carregar bairros: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_ranking_bairros(cidade_id: str = None, limite: int = 20) -> pd.DataFrame:
    """
    Busca ranking de bairros com score composto.
    Score = (40% valorizacao) + (35% demanda) + (25% oferta)

    Uses view: vw_ranking_bairros

    Args:
        cidade_id (str): ID da cidade ou None
        limite (int): Limitar resultado a N bairros

    Returns:
        pd.DataFrame: DataFrame com ranking
    """
    try:
        client = get_supabase_client()
        query = client.table("vw_ranking_bairros").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.order("score_composto", desc=True).limit(limite).execute()

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar ranking de bairros: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_PROFILE)
def get_bairro_por_id(bairro_id: str) -> dict:
    """
    Busca dados detalhados de um bairro.

    Args:
        bairro_id (str): ID do bairro (UUID)

    Returns:
        dict: Dados do bairro
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("bairros")
            .select("*")
            .eq("id", bairro_id)
            .single()
            .execute()
        )

        return response.data if response.data else {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar bairro: {str(e)}")
        return {}


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_bairros_por_cidade(cidade_nome: str) -> dict:
    """
    Busca todos os bairros de uma cidade e retorna como dicionário.

    Args:
        cidade_nome (str): Nome da cidade

    Returns:
        dict: {bairro_id: bairro_nome}
    """
    try:
        client = get_supabase_client()

        # Primeiro, encontrar a cidade
        cidade_response = (
            client.table("cidades")
            .select("id")
            .eq("nome", cidade_nome)
            .single()
            .execute()
        )

        if not cidade_response.data:
            return {}

        cidade_id = cidade_response.data["id"]

        # Depois, buscar bairros dessa cidade
        response = (
            client.table("bairros")
            .select("id,nome")
            .eq("cidade_id", cidade_id)
            .order("nome")
            .execute()
        )

        # Converter em dicionário {id: nome}
        return {item["id"]: item["nome"] for item in response.data}
    except Exception as e:
        st.error(f"❌ Erro ao carregar bairros da cidade: {str(e)}")
        return {}


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_cidades_list() -> list:
    """
    Retorna lista de nomes de cidades para filtro.

    Returns:
        list: Lista de nomes de cidades
    """
    try:
        client = get_supabase_client()
        response = client.table("cidades").select("nome").order("nome").execute()
        return [item["nome"] for item in response.data]
    except Exception as e:
        st.error(f"❌ Erro ao carregar cidades: {str(e)}")
        return []


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_top_bairros_por_score(
    cidade_id: str = None, limite: int = 5
) -> pd.DataFrame:
    """
    Busca os top N bairros por score composto.

    Args:
        cidade_id (str): ID da cidade ou None
        limite (int): Número de bairros a retornar

    Returns:
        pd.DataFrame: Top bairros
    """
    df = get_ranking_bairros(cidade_id=cidade_id, limite=limite)
    return df


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_bairro_stats(bairro_id: str) -> dict:
    """
    Busca estatísticas de um bairro (score composto, total de imóveis, etc).

    Args:
        bairro_id (str): ID do bairro

    Returns:
        dict: Estatísticas do bairro
    """
    try:
        # Buscar dados do bairro
        client = get_supabase_client()

        # Usar a view vw_ranking_bairros para obter score composto
        response = (
            client.table("vw_ranking_bairros")
            .select("*")
            .eq("id", bairro_id)
            .single()
            .execute()
        )

        if response.data:
            return response.data
        else:
            return {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar stats do bairro: {str(e)}")
        return {}
