"""
Service para dados de imóveis
"""

import streamlit as st
import pandas as pd
from services.supabase_client import get_supabase_client
from config import settings


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_all_imoveis(cidade_id: str = None, bairro_id: str = None) -> pd.DataFrame:
    """
    Busca todos os imóveis, opcionalmente filtrados.

    Args:
        cidade_id (str): ID da cidade (UUID) ou None
        bairro_id (str): ID do bairro (UUID) ou None

    Returns:
        pd.DataFrame: DataFrame com imóveis
    """
    try:
        client = get_supabase_client()
        query = client.table("imoveis").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        if bairro_id:
            query = query.eq("bairro_id", bairro_id)

        response = query.execute()
        df = pd.DataFrame(response.data)

        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóveis: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imoveis_com_filtros(
    cidade_id: str = None,
    bairro_id: str = None,
    preco_min: float = 0,
    preco_max: float = 999999999,
) -> pd.DataFrame:
    """
    Busca imóveis com filtros de cidade, bairro e faixa de preço.

    Args:
        cidade_id (str): ID da cidade ou None
        bairro_id (str): ID do bairro ou None
        preco_min (float): Preço mínimo
        preco_max (float): Preço máximo

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df = get_all_imoveis(cidade_id=cidade_id, bairro_id=bairro_id)

    if not df.empty:
        df = df[
            (df["preco"] >= preco_min) & (df["preco"] <= preco_max)
        ].copy()

    return df.sort_values("preco")


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imoveis_marketing_fraco(
    score_minimo: float = 40, cidade_id: str = None
) -> pd.DataFrame:
    """
    Busca imóveis com marketing fraco (score > score_minimo).
    Usa a view vw_imoveis_marketing_fraco do Supabase.

    Args:
        score_minimo (float): Score mínimo de fraqueza (0-100)
        cidade_id (str): ID da cidade ou None

    Returns:
        pd.DataFrame: DataFrame com imóveis ordenados por score DESC
    """
    try:
        client = get_supabase_client()
        query = (
            client.table("vw_imoveis_marketing_fraco")
            .select("*")
            .gte("score_fraqueza_marketing", score_minimo)
        )

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.order("score_fraqueza_marketing", desc=True).execute()

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóveis com marketing fraco: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_PROFILE)
def get_imovel_por_id(imovel_id: str) -> dict:
    """
    Busca dados detalhados de um imóvel.

    Args:
        imovel_id (str): ID do imóvel (UUID)

    Returns:
        dict: Dados do imóvel
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("imoveis")
            .select("*")
            .eq("id", imovel_id)
            .single()
            .execute()
        )

        return response.data if response.data else {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóvel: {str(e)}")
        return {}


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imoveis_por_empreendimento(
    tipo_empreendimento: str, cidade_id: str = None
) -> pd.DataFrame:
    """
    Busca imóveis filtrados por tipo de empreendimento.

    Args:
        tipo_empreendimento (str): Tipo ('projeto', 'fundações', 'estrutura', 'acabamento', 'pronto')
        cidade_id (str): ID da cidade ou None

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    try:
        client = get_supabase_client()
        query = (
            client.table("imoveis")
            .select("*")
            .eq("tipo_empreendimento", tipo_empreendimento)
        )

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóveis por empreendimento: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imoveis_em_construcao(cidade_id: str = None) -> pd.DataFrame:
    """
    Busca imóveis em construção.

    Args:
        cidade_id (str): ID da cidade ou None

    Returns:
        pd.DataFrame: DataFrame com imóveis em construção
    """
    try:
        client = get_supabase_client()
        query = client.table("imoveis").select("*").eq("em_construcao", True)

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóveis em construção: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def count_imoveis_total() -> int:
    """
    Conta total de imóveis cadastrados.

    Returns:
        int: Total de imóveis
    """
    try:
        client = get_supabase_client()
        response = client.table("imoveis").select("id", count="exact").execute()
        return response.count or 0
    except:
        return 0


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_preco_medio_imoveis(cidade_id: str = None) -> float:
    """
    Calcula preço médio dos imóveis.

    Args:
        cidade_id (str): ID da cidade ou None

    Returns:
        float: Preço médio
    """
    df = get_all_imoveis(cidade_id=cidade_id)

    if df.empty or "preco" not in df.columns:
        return 0.0

    return float(df["preco"].mean())
