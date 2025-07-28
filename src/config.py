import os
from typing import Optional
from supabase import create_client, Client

class Settings:
    """Configurações da aplicação"""
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MyFinance"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://myfinance.vercel.app",
        "https://myfinance-frontend.vercel.app"
    ]
    
    @property
    def supabase_client(self) -> Client:
        """Retorna cliente do Supabase"""
        if not self.SUPABASE_URL or not self.SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_ANON_KEY devem ser configurados")
        
        return create_client(self.SUPABASE_URL, self.SUPABASE_ANON_KEY)

# Instância global das configurações
settings = Settings() 