"""
Configurações centralizadas da aplicação
Lê do arquivo .env usando python-dotenv
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class Settings:
    """Classe com todas as configurações da aplicação"""

    # ========================================
    # Supabase
    # ========================================
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # ========================================
    # Mapbox
    # ========================================
    MAPBOX_TOKEN: str = os.getenv("MAPBOX_TOKEN", "")

    # ========================================
    # App Configuration
    # ========================================
    APP_NAME: str = "Dashboard de Inteligência Imobiliária"
    APP_ICON: str = "🏠"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # ========================================
    # Cache Configuration
    # ========================================
    CACHE_TTL_SECONDS: int = 120  # 2 minutos
    CACHE_TTL_PROFILE: int = 300  # 5 minutos

    # ========================================
    # Validações
    # ========================================
    @staticmethod
    def validate():
        """Valida se as configurações críticas estão presentes"""
        errors = []

        if not Settings.SUPABASE_URL:
            errors.append("❌ SUPABASE_URL não configurada no .env")

        if not Settings.SUPABASE_ANON_KEY:
            errors.append("❌ SUPABASE_ANON_KEY não configurada no .env")

        if not Settings.MAPBOX_TOKEN:
            errors.append("⚠️  MAPBOX_TOKEN não configurada no .env (mapas desabilitados)")

        return errors

    @staticmethod
    def check_critical():
        """Retorna apenas erros críticos (Supabase)"""
        errors = []

        if not Settings.SUPABASE_URL:
            errors.append("SUPABASE_URL")

        if not Settings.SUPABASE_ANON_KEY:
            errors.append("SUPABASE_ANON_KEY")

        return errors


# Exportar instância global de configurações
settings = Settings()
