"""
Middleware de segurança para FastAPI

Este módulo implementa middlewares para adicionar cabeçalhos de segurança
e Content Security Policy (CSP) à aplicação FastAPI.
"""

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Dict
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware para adicionar cabeçalhos de segurança às respostas HTTP"""
    
    def __init__(
        self,
        app: FastAPI,
        csp_policy: Dict[str, str] = None,
        hsts_max_age: int = 31536000,  # 1 ano em segundos
        include_subdomains: bool = True,
        preload: bool = False,
        xss_protection: bool = True,
        content_type_options: bool = True,
        frame_options: str = "DENY",
        referrer_policy: str = "strict-origin-when-cross-origin",
        permissions_policy: str = None
    ):
        super().__init__(app)
        self.csp_policy = csp_policy or {
            "default-src": "'self'",
            "script-src": "'self'",
            "style-src": "'self'",
            "img-src": "'self' data:",
            "font-src": "'self'",
            "connect-src": "'self'",
            "frame-src": "'none'",
            "object-src": "'none'",
            "base-uri": "'self'",
            "form-action": "'self'"
        }
        self.hsts_max_age = hsts_max_age
        self.include_subdomains = include_subdomains
        self.preload = preload
        self.xss_protection = xss_protection
        self.content_type_options = content_type_options
        self.frame_options = frame_options
        self.referrer_policy = referrer_policy
        self.permissions_policy = permissions_policy
        
        logger.info("SecurityHeadersMiddleware inicializado com CSP e cabeçalhos de segurança")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Content-Security-Policy
        if self.csp_policy:
            csp_header = "; ".join([f"{key} {value}" for key, value in self.csp_policy.items()])
            response.headers["Content-Security-Policy"] = csp_header
        
        # Strict-Transport-Security (HSTS)
        hsts_value = f"max-age={self.hsts_max_age}"
        if self.include_subdomains:
            hsts_value += "; includeSubDomains"
        if self.preload:
            hsts_value += "; preload"
        response.headers["Strict-Transport-Security"] = hsts_value
        
        # X-XSS-Protection
        if self.xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # X-Content-Type-Options
        if self.content_type_options:
            response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-Frame-Options
        if self.frame_options:
            response.headers["X-Frame-Options"] = self.frame_options
        
        # Referrer-Policy
        if self.referrer_policy:
            response.headers["Referrer-Policy"] = self.referrer_policy
        
        # Permissions-Policy
        if self.permissions_policy:
            response.headers["Permissions-Policy"] = self.permissions_policy
        
        return response

def add_security_middleware(app: FastAPI, **kwargs) -> None:
    """Adiciona o middleware de segurança à aplicação FastAPI
    
    Args:
        app: Instância da aplicação FastAPI
        **kwargs: Argumentos para configurar o middleware SecurityHeadersMiddleware
    """
    app.add_middleware(SecurityHeadersMiddleware, **kwargs)