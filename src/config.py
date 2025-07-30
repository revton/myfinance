import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Settings:
    """Configurações da aplicação"""
    
    # Ambiente
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Supabase - Configuração baseada no ambiente
    def _get_supabase_config(self) -> tuple[str, str]:
        """Retorna configuração do Supabase baseada no ambiente"""
        if self.ENVIRONMENT == "production":
            url = os.getenv("SUPABASE_PROD_URL", "")
            key = os.getenv("SUPABASE_PROD_ANON_KEY", "")
        else:  # development (padrão)
            url = os.getenv("SUPABASE_URL", "")
            key = os.getenv("SUPABASE_ANON_KEY", "")
        
        return url, key
    
    @property
    def SUPABASE_URL(self) -> str:
        """URL do Supabase baseada no ambiente"""
        return self._get_supabase_config()[0]
    
    @property
    def SUPABASE_ANON_KEY(self) -> str:
        """Chave anônima do Supabase baseada no ambiente"""
        return self._get_supabase_config()[1]
    
    # Database - Configuração baseada no ambiente
    def _get_database_url(self) -> Optional[str]:
        """Retorna URL do banco baseada no ambiente"""
        if self.ENVIRONMENT == "production":
            return os.getenv("DATABASE_PROD_URL")
        else:  # development (padrão)
            return os.getenv("DATABASE_URL")
    
    @property
    def DATABASE_URL(self) -> Optional[str]:
        """URL do banco de dados baseada no ambiente"""
        return self._get_database_url()
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MyFinance"
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://myfinance.vercel.app",
        "https://myfinance-frontend.vercel.app"
    ]
    
    # Logs
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        self._supabase_client = None
    
    @property
    def supabase_client(self) -> Client:
        """Retorna cliente do Supabase"""
        # Se já existe um cliente cached, retorna ele
        if self._supabase_client is not None:
            return self._supabase_client
            
        # Verifica se as variáveis de ambiente estão configuradas
        if not self.SUPABASE_URL or not self.SUPABASE_ANON_KEY:
            raise ValueError(
                f"Configuração do Supabase não encontrada para ambiente '{self.ENVIRONMENT}'. "
                f"Configure SUPABASE_{self.ENVIRONMENT.upper()}_URL e "
                f"SUPABASE_{self.ENVIRONMENT.upper()}_ANON_KEY no arquivo .env"
            )
        
        # Cria e cache o cliente
        self._supabase_client = create_client(self.SUPABASE_URL, self.SUPABASE_ANON_KEY)
        return self._supabase_client
    
    def set_mock_supabase_client(self, mock_client):
        """Método para definir um cliente mock durante os testes"""
        self._supabase_client = mock_client

# Instância global das configurações
settings = Settings() 