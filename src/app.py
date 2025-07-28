"""
MyFinance Flask Application
Sistema de gestão financeira pessoal com Flask e sistema de migrações
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
import os
from typing import Dict, Any

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name: str = 'default') -> Flask:
    """Factory function para criar a aplicação Flask"""
    
    app = Flask(__name__)
    
    # Configuração da aplicação
    app.config.from_object(get_config(config_name))
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Registrar comandos CLI para migrações
    register_cli_commands(app)
    
    return app

def get_config(config_name: str) -> object:
    """Retorna a configuração baseada no ambiente"""
    
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    
    return configs.get(config_name, DevelopmentConfig)

class BaseConfig:
    """Configuração base da aplicação"""
    
    # Projeto
    PROJECT_NAME = "MyFinance"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://myfinance.vercel.app",
        "https://myfinance-frontend.vercel.app"
    ]
    
    # Supabase (opcional para compatibilidade)
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

class DevelopmentConfig(BaseConfig):
    """Configuração para desenvolvimento"""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        'postgresql://user:password@localhost/myfinance_dev'
    )

class TestingConfig(BaseConfig):
    """Configuração para testes"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(BaseConfig):
    """Configuração para produção"""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Configurações de segurança para produção
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

def register_cli_commands(app: Flask):
    """Registra comandos CLI personalizados"""
    
    @app.cli.command()
    def init_db():
        """Inicializa o banco de dados"""
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
    
    @app.cli.command()
    def reset_db():
        """Reseta o banco de dados (CUIDADO!)"""
        if input("⚠️  Tem certeza que quer resetar o banco? (y/N): ").lower() == 'y':
            db.drop_all()
            db.create_all()
            print("✅ Banco de dados resetado com sucesso!")
        else:
            print("❌ Operação cancelada")
    
    @app.cli.command()
    def seed_db():
        """Adiciona dados de exemplo ao banco"""
        from .models import Transaction
        
        # Verificar se já existem dados
        if Transaction.query.first():
            print("ℹ️  Banco já contém dados. Use reset_db primeiro se necessário.")
            return
        
        # Dados de exemplo
        sample_transactions = [
            Transaction(
                type='income',
                amount=2500.00,
                description='Salário Janeiro'
            ),
            Transaction(
                type='expense',
                amount=350.00,
                description='Supermercado'
            ),
            Transaction(
                type='expense',
                amount=80.00,
                description='Combustível'
            ),
            Transaction(
                type='income',
                amount=200.00,
                description='Freelance'
            ),
            Transaction(
                type='expense',
                amount=1200.00,
                description='Aluguel'
            )
        ]
        
        # Adicionar ao banco
        for transaction in sample_transactions:
            db.session.add(transaction)
        
        db.session.commit()
        print(f"✅ {len(sample_transactions)} transações de exemplo adicionadas!")
    
    @app.cli.command()
    def status():
        """Mostra o status da aplicação e banco de dados"""
        from .models import Transaction
        
        print(f"🚀 {app.config['PROJECT_NAME']} - Status da Aplicação")
        print("=" * 50)
        print(f"🔧 Ambiente: {app.config.get('ENV', 'development')}")
        print(f"🗄️  Database: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        print(f"🔒 Debug: {app.config['DEBUG']}")
        
        try:
            total_transactions = Transaction.query.count()
            income_total = db.session.query(db.func.sum(Transaction.amount)).filter(
                Transaction.type == 'income'
            ).scalar() or 0
            expense_total = db.session.query(db.func.sum(Transaction.amount)).filter(
                Transaction.type == 'expense'
            ).scalar() or 0
            
            print(f"📊 Total de transações: {total_transactions}")
            print(f"💰 Total de receitas: R$ {income_total:.2f}")
            print(f"💸 Total de despesas: R$ {expense_total:.2f}")
            print(f"💵 Saldo atual: R$ {income_total - expense_total:.2f}")
            print("✅ Conexão com banco de dados OK")
            
        except Exception as e:
            print(f"❌ Erro ao conectar com banco: {e}")

# Criar instância da aplicação para desenvolvimento
app = create_app(os.environ.get('FLASK_ENV', 'development'))