"""
Service para dados de investidores detectados
"""

import streamlit as st
import pandas as pd
from services.supabase_client import get_supabase_client
from config import settings


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_all_investidores(cidade_id: str = None) -> pd.DataFrame:
    """
    Busca todos os investidores, opcionalmente filtrados por cidade.

    Args:
        cidade_id (str): ID da cidade (UUID) ou None

    Returns:
        pd.DataFrame: DataFrame com investidores
    """
    try:
        client = get_supabase_client()
        query = client.table("investidores_detectados").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = query.execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar investidores: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_top_investidores(limite: int = 50, cidade_id: str = None) -> pd.DataFrame:
    """
    Busca os top N investidores por quantidade de imóveis.

    Args:
        limite (int): Quantidade máxima
        cidade_id (str): ID da cidade ou None

    Returns:
        pd.DataFrame: Top investidores
    """
    try:
        client = get_supabase_client()

        # Usar view vw_investidores_resumo
        query = client.table("vw_investidores_resumo").select("*")

        if cidade_id:
            query = query.eq("cidade_id", cidade_id)

        response = (
            query.order("qtd_imoveis", desc=True)
            .limit(limite)
            .execute()
        )

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar top investidores: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_PROFILE)
def get_investidor_por_id(investidor_id: str) -> dict:
    """
    Busca dados detalhados de um investidor.

    Args:
        investidor_id (str): ID do investidor (UUID)

    Returns:
        dict: Dados do investidor
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("investidores_detectados")
            .select("*")
            .eq("id", investidor_id)
            .single()
            .execute()
        )

        return response.data if response.data else {}
    except Exception as e:
        st.error(f"❌ Erro ao carregar investidor: {str(e)}")
        return {}


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_imoveis_por_investidor(investidor_id: str) -> pd.DataFrame:
    """
    Busca todos os imóveis de um investidor.

    Args:
        investidor_id (str): ID do investidor (UUID)

    Returns:
        pd.DataFrame: DataFrame com imóveis do investidor
    """
    try:
        client = get_supabase_client()

        # Buscar via tabela de relacionamento
        response = (
            client.table("investidores_imoveis")
            .select("imovel_id, data_compra, preco_compra")
            .eq("investidor_id", investidor_id)
            .execute()
        )

        imovel_ids = [item["imovel_id"] for item in response.data]

        if not imovel_ids:
            return pd.DataFrame()

        # Buscar dados dos imóveis
        imoveis_response = (
            client.table("imoveis")
            .select("*")
            .in_("id", imovel_ids)
            .execute()
        )

        df = pd.DataFrame(imoveis_response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar imóveis do investidor: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_investidores_por_bairro(bairro_nome: str) -> pd.DataFrame:
    """
    Busca investidores que preferem um bairro específico.

    Args:
        bairro_nome (str): Nome do bairro

    Returns:
        pd.DataFrame: DataFrame com investidores
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("investidores_detectados")
            .select("*")
            .eq("bairro_preferido", bairro_nome)
            .order("qtd_imoveis", desc=True)
            .execute()
        )

        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar investidores por bairro: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def count_investidores_total() -> int:
    """
    Conta total de investidores cadastrados.

    Returns:
        int: Total de investidores
    """
    try:
        client = get_supabase_client()
        response = (
            client.table("investidores_detectados")
            .select("id", count="exact")
            .execute()
        )
        return response.count or 0
    except:
        return 0


@st.cache_data(ttl=settings.CACHE_TTL_SECONDS)
def get_investidor_valor_medio() -> float:
    """
    Calcula valor médio investido por investidor.

    Returns:
        float: Valor médio
    """
    df = get_all_investidores()

    if df.empty or "valor_total_investido" not in df.columns:
        return 0.0

    return float(df["valor_total_investido"].mean())
