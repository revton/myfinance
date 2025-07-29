#!/usr/bin/env python3
"""
Script para migrar dados do Supabase para Flask + SQLAlchemy
Migra todas as transações existentes preservando dados e timestamps
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def migrate_data():
    """Migra dados do Supabase para SQLAlchemy"""
    
    print("🔄 Iniciando migração de dados: Supabase → Flask")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    database_url = os.getenv('DATABASE_URL')
    
    if not all([supabase_url, supabase_key, database_url]):
        print("❌ Variáveis de ambiente faltando:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_ANON_KEY") 
        print("   - DATABASE_URL")
        return False
    
    try:
        # Import Supabase
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conectado ao Supabase")
        
        # Import Flask app
        from src.app import create_app, db
        from src.models import Transaction
        
        app = create_app('production' if 'production' in database_url else 'development')
        
        with app.app_context():
            print("✅ Conectado ao PostgreSQL/SQLAlchemy")
            
            # Verificar se banco está inicializado
            try:
                db.create_all()
                print("✅ Estrutura do banco verificada")
            except Exception as e:
                print(f"❌ Erro na estrutura do banco: {e}")
                return False
            
            # Buscar dados do Supabase
            print("\n📊 Buscando dados do Supabase...")
            try:
                result = supabase.table("transactions").select("*").order("created_at").execute()
                supabase_transactions = result.data
                print(f"✅ {len(supabase_transactions)} transações encontradas no Supabase")
                
                if not supabase_transactions:
                    print("ℹ️  Nenhuma transação para migrar")
                    return True
                    
            except Exception as e:
                print(f"❌ Erro ao buscar dados do Supabase: {e}")
                return False
            
            # Verificar dados existentes no SQLAlchemy
            existing_count = Transaction.query.count()
            if existing_count > 0:
                print(f"⚠️  Já existem {existing_count} transações no banco SQLAlchemy")
                confirm = input("Continuar migração? (y/N): ")
                if confirm.lower() != 'y':
                    print("❌ Migração cancelada")
                    return False
            
            # Migrar dados
            print("\n🔄 Migrando transações...")
            migrated_count = 0
            errors = []
            
            for item in supabase_transactions:
                try:
                    # Verificar se transação já existe (por ID se disponível)
                    existing = None
                    if 'id' in item:
                        existing = Transaction.query.filter_by(id=item['id']).first()
                    
                    if existing:
                        print(f"⏭️  Transação {item['id']} já existe, pulando...")
                        continue
                    
                    # Criar nova transação
                    transaction_data = {
                        'type': item['type'],
                        'amount': Decimal(str(item['amount'])),
                        'description': item['description']
                    }
                    
                    # Se tiver ID do Supabase, preservar
                    if 'id' in item:
                        transaction_data['id'] = item['id']
                    
                    transaction = Transaction(**transaction_data)
                    
                    # Preservar timestamps se existirem
                    if 'created_at' in item and item['created_at']:
                        transaction.created_at = datetime.fromisoformat(
                            item['created_at'].replace('Z', '+00:00')
                        )
                    
                    if 'updated_at' in item and item['updated_at']:
                        transaction.updated_at = datetime.fromisoformat(
                            item['updated_at'].replace('Z', '+00:00')
                        )
                    
                    db.session.add(transaction)
                    migrated_count += 1
                    
                    # Commit em lotes de 50
                    if migrated_count % 50 == 0:
                        db.session.commit()
                        print(f"   ✅ {migrated_count} transações migradas...")
                    
                except Exception as e:
                    error_msg = f"Erro na transação {item.get('id', 'unknown')}: {e}"
                    errors.append(error_msg)
                    print(f"   ❌ {error_msg}")
                    continue
            
            # Commit final
            try:
                db.session.commit()
                print(f"\n✅ Migração concluída!")
                print(f"   📊 {migrated_count} transações migradas com sucesso")
                
                if errors:
                    print(f"   ⚠️  {len(errors)} erros encontrados:")
                    for error in errors[:5]:  # Mostrar apenas os primeiros 5
                        print(f"      - {error}")
                    if len(errors) > 5:
                        print(f"      ... e mais {len(errors) - 5} erros")
                
                # Verificar dados migrados
                final_count = Transaction.query.count()
                print(f"\n📊 Total de transações no banco: {final_count}")
                
                # Mostrar resumo
                summary = Transaction.get_summary()
                print(f"💰 Total de receitas: R$ {summary['total_income']:.2f}")
                print(f"💸 Total de despesas: R$ {summary['total_expense']:.2f}")
                print(f"💵 Saldo atual: R$ {summary['balance']:.2f}")
                
                return True
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao salvar dados: {e}")
                return False
                
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Instale as dependências: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def validate_migration():
    """Valida se a migração foi bem-sucedida"""
    
    print("\n🔍 Validando migração...")
    
    try:
        from src.app import create_app, db
        from src.models import Transaction
        
        app = create_app()
        with app.app_context():
            # Contar transações
            total = Transaction.query.count()
            income_count = Transaction.query.filter_by(type='income').count()
            expense_count = Transaction.query.filter_by(type='expense').count()
            
            print(f"✅ Total de transações: {total}")
            print(f"✅ Receitas: {income_count}")
            print(f"✅ Despesas: {expense_count}")
            
            # Verificar integridade
            if income_count + expense_count != total:
                print("❌ Erro de integridade nos tipos")
                return False
            
            # Verificar se há transações com valores inválidos
            invalid_amounts = Transaction.query.filter(Transaction.amount <= 0).count()
            if invalid_amounts > 0:
                print(f"❌ {invalid_amounts} transações com valores inválidos")
                return False
            
            print("✅ Validação concluída com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ MyFinance - Migração de Dados Supabase → Flask")
    print("=" * 55)
    
    # Executar migração
    success = migrate_data()
    
    if success:
        # Validar migração
        validate_migration()
        print("\n🎉 Migração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Testar API Flask: python run_flask.py")
        print("2. Executar testes: pytest tests/test_flask_app.py")
        print("3. Configurar frontend para nova URL (se necessário)")
        print("4. Fazer backup dos dados do Supabase")
        print("5. Atualizar variáveis de ambiente do deploy")
    else:
        print("\n🚨 Migração falhou!")
        print("Verifique os erros acima e tente novamente")
        sys.exit(1)