"""Módulo de serviços de dados"""

from .supabase_client import get_supabase_client, test_connection, get_table
from . import imobiliarias_service
from . import imoveis_service
from . import bairros_service
from . import investidores_service
from . import prospeccao_service

__all__ = [
    "get_supabase_client",
    "test_connection",
    "get_table",
    "imobiliarias_service",
    "imoveis_service",
    "bairros_service",
    "investidores_service",
    "prospeccao_service",
]
