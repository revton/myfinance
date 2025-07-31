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
    
    # Supabase - Configuração única baseada no ambiente atual
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
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
        "https://myfinance-frontend.vercel.app",
        "https://myfinance-three.vercel.app",  # URL atual do frontend em produção
        "https://myfinance-backend-xcct.onrender.com"  # URL atual do backend em produção
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
                f"Configure SUPABASE_URL e SUPABASE_ANON_KEY no arquivo .env "
                f"para o ambiente '{self.ENVIRONMENT}'"
            )
        
        # Cria e cache o cliente
        self._supabase_client = create_client(self.SUPABASE_URL, self.SUPABASE_ANON_KEY)
        return self._supabase_client
    
    @supabase_client.setter
    def supabase_client(self, value):
        """Setter para permitir mocking nos testes"""
        self._supabase_client = value
    
    @supabase_client.deleter
    def supabase_client(self):
        """Deleter para permitir mocking nos testes"""
        self._supabase_client = None
    
    def set_mock_supabase_client(self, mock_client):
        """Método para definir um cliente mock durante os testes"""
        self._supabase_client = mock_client

# Instância global das configurações
settings = Settings() 