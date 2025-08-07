#!/usr/bin/env python3
"""
Script para listar todas as rotas disponíveis na API
Execute: uv run python scripts/list_routes.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def list_routes():
    """
    Lista todas as rotas disponíveis na API
    """
    print("🔍 Listando Rotas da API")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Buscar OpenAPI JSON
            print("🔄 Buscando especificação OpenAPI...")
            openapi_response = await client.get(
                f"{api_base_url}/openapi.json",
                timeout=30.0
            )
            
            if openapi_response.status_code == 200:
                openapi_data = openapi_response.json()
                paths = openapi_data.get("paths", {})
                
                print("✅ Rotas encontradas:")
                print()
                
                # Agrupar por tags
                routes_by_tag = {}
                
                for path, methods in paths.items():
                    for method, details in methods.items():
                        if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                            tags = details.get("tags", ["Sem tag"])
                            for tag in tags:
                                if tag not in routes_by_tag:
                                    routes_by_tag[tag] = []
                                routes_by_tag[tag].append({
                                    "method": method.upper(),
                                    "path": path,
                                    "summary": details.get("summary", "Sem descrição")
                                })
                
                # Exibir rotas organizadas por tag
                for tag, routes in routes_by_tag.items():
                    print(f"📂 {tag.upper()}:")
                    for route in routes:
                        method_color = {
                            "GET": "🟢",
                            "POST": "🔵", 
                            "PUT": "🟡",
                            "DELETE": "🔴",
                            "PATCH": "🟠"
                        }.get(route["method"], "⚪")
                        
                        print(f"   {method_color} {route['method']} {route['path']}")
                        print(f"      📝 {route['summary']}")
                    print()
                
                # Resumo
                total_routes = sum(len(routes) for routes in routes_by_tag.values())
                print(f"📊 Total de rotas: {total_routes}")
                print(f"📂 Total de tags: {len(routes_by_tag)}")
                
            else:
                print(f"❌ Erro ao buscar OpenAPI: {openapi_response.status_code}")
                print(f"   Response: {openapi_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

async def test_specific_routes():
    """
    Testa rotas específicas de autenticação
    """
    print("\n🧪 Testando Rotas de Autenticação")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    test_routes = [
        ("GET", "/health", "Health Check"),
        ("POST", "/auth/register", "Registro"),
        ("POST", "/auth/login", "Login"),
        ("POST", "/auth/forgot-password", "Recuperação de Senha"),
        ("POST", "/auth/reset-password", "Reset de Senha"),
        ("GET", "/auth/profile", "Perfil do Usuário"),
        ("PUT", "/auth/profile", "Atualizar Perfil"),
        ("DELETE", "/auth/profile", "Deletar Perfil")
    ]
    
    try:
        async with httpx.AsyncClient() as client:
            for method, path, description in test_routes:
                print(f"🔄 Testando {method} {path}...")
                
                try:
                    if method == "GET":
                        response = await client.get(f"{api_base_url}{path}", timeout=10.0)
                    elif method == "POST":
                        response = await client.post(f"{api_base_url}{path}", timeout=10.0)
                    elif method == "PUT":
                        response = await client.put(f"{api_base_url}{path}", timeout=10.0)
                    elif method == "DELETE":
                        response = await client.delete(f"{api_base_url}{path}", timeout=10.0)
                    
                    status_emoji = "✅" if response.status_code < 400 else "⚠️"
                    print(f"   {status_emoji} {response.status_code} - {description}")
                    
                except Exception as e:
                    print(f"   ❌ Erro: {str(e)}")
                    
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Listador de Rotas da API")
    print("💡 Mostra todas as rotas disponíveis e testa as principais")
    print()
    
    await list_routes()
    await test_specific_routes()
    
    print("\n🎉 Análise concluída!")
    print("💡 Dica: Use o Swagger UI em http://localhost:8002/docs para testar as rotas")

if __name__ == "__main__":
    asyncio.run(main()) 