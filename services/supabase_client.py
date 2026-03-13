"""
Cliente Supabase com cache de sessão (singleton)
Mantém uma única conexão durante toda a sessão do Streamlit
"""

import streamlit as st
from supabase import create_client
from config import settings


@st.cache_resource
def get_supabase_client():
    """
    Retorna cliente Supabase como singleton.
    Decorado com @st.cache_resource para manter apenas uma conexão por sessão.

    Returns:
        supabase.Client: Cliente conectado ao Supabase

    Raises:
        ValueError: Se credenciais estão faltando
    """
    # Validar configurações críticas
    missing = settings.check_critical()
    if missing:
        raise ValueError(
            f"❌ Configurações obrigatórias faltando: {', '.join(missing)}\n"
            f"Adicione-as ao arquivo .env"
        )

    try:
        client = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_ANON_KEY,
        )
        return client
    except Exception as e:
        raise ValueError(f"❌ Erro ao conectar ao Supabase: {str(e)}")


def test_connection() -> dict:
    """
    Testa a conexão com Supabase.

    Returns:
        dict: {'success': bool, 'message': str, 'stats': dict}
    """
    try:
        client = get_supabase_client()

        # Teste simples: contar cidades
        response = client.table("cidades").select("id", count="exact").execute()

        cidades_count = response.count or 0

        # Contar bairros
        response_bairros = (
            client.table("bairros").select("id", count="exact").execute()
        )
        bairros_count = response_bairros.count or 0

        # Contar imóveis
        response_imoveis = (
            client.table("imoveis").select("id", count="exact").execute()
        )
        imoveis_count = response_imoveis.count or 0

        return {
            "success": True,
            "message": "✅ Conectado ao Supabase com sucesso",
            "stats": {
                "cidades": cidades_count,
                "bairros": bairros_count,
                "imoveis": imoveis_count,
            },
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Erro ao conectar: {str(e)}",
            "stats": None,
        }


def get_table(table_name: str):
    """
    Acesso rápido a uma tabela Supabase.

    Args:
        table_name (str): Nome da tabela

    Returns:
        postgrest.SyncQuery: Query builder da tabela
    """
    client = get_supabase_client()
    return client.table(table_name)
