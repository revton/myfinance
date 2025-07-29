#!/usr/bin/env python3
"""
Script para executar a aplicação Flask MyFinance
Para desenvolvimento local
"""

import os
from src.app import create_app

if __name__ == '__main__':
    # Configurar variáveis de ambiente para desenvolvimento
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    # Criar e executar a aplicação
    app = create_app('development')
    
    print("🚀 Iniciando MyFinance Flask Application...")
    print("📍 URL: http://localhost:5000")
    print("📋 Endpoints disponíveis:")
    print("   - GET  /api/v1/health")
    print("   - GET  /api/v1/status")
    print("   - GET  /api/v1/transactions/")
    print("   - POST /api/v1/transactions/")
    print("   - GET  /api/v1/summary")
    print("   - GET  /api/v1/balance")
    print("\n🔧 Para usar comandos CLI:")
    print("   flask --app src.app init_db")
    print("   flask --app src.app seed_db")
    print("   flask --app src.app status")
    print("\n⏹️  Para parar: Ctrl+C")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )