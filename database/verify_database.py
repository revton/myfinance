#!/usr/bin/env python3
"""
Script para verificar a configuração do banco de dados Supabase
Útil para debug e troubleshooting
"""

import os
from supabase import create_client
from datetime import datetime

def verify_database():
    """Verifica a conexão e estrutura do banco de dados"""
    
    print("🔍 Verificando configuração do banco de dados...")
    print("=" * 50)
    
    # 1. Verificar variáveis de ambiente
    print("1. Verificando variáveis de ambiente:")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url:
        print("❌ SUPABASE_URL não encontrada")
        return False
    else:
        print(f"✅ SUPABASE_URL: {supabase_url[:30]}...")
    
    if not supabase_key:
        print("❌ SUPABASE_ANON_KEY não encontrada")
        return False
    else:
        print(f"✅ SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    
    print()
    
    # 2. Testar conexão
    print("2. Testando conexão com Supabase:")
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conexão estabelecida com sucesso")
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
    
    print()
    
    # 3. Verificar se a tabela existe
    print("3. Verificando tabela 'transactions':")
    
    try:
        # Tentar fazer uma consulta simples
        result = supabase.table("transactions").select("*").limit(1).execute()
        print("✅ Tabela 'transactions' encontrada")
        print(f"✅ Estrutura da resposta: {type(result.data)}")
        
        if result.data:
            print(f"✅ Dados existem: {len(result.data)} registro(s) encontrado(s)")
            print(f"✅ Exemplo de registro: {result.data[0]}")
        else:
            print("ℹ️  Tabela existe mas está vazia")
            
    except Exception as e:
        print(f"❌ Erro ao acessar tabela 'transactions': {e}")
        print("💡 Dica: Execute o script create_tables.sql no Supabase SQL Editor")
        return False
    
    print()
    
    # 4. Testar operações CRUD
    print("4. Testando operações CRUD:")
    
    # Criar uma transação de teste
    test_transaction = {
        "type": "expense",
        "amount": 1.00,
        "description": f"Teste de conexão - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    try:
        # CREATE
        create_result = supabase.table("transactions").insert(test_transaction).execute()
        if create_result.data:
            test_id = create_result.data[0]['id']
            print("✅ CREATE: Transação de teste criada")
            
            # READ
            read_result = supabase.table("transactions").select("*").eq("id", test_id).execute()
            if read_result.data:
                print("✅ READ: Transação de teste lida")
                
                # UPDATE
                update_data = {"description": "Teste de conexão - ATUALIZADO"}
                update_result = supabase.table("transactions").update(update_data).eq("id", test_id).execute()
                if update_result.data:
                    print("✅ UPDATE: Transação de teste atualizada")
                    
                    # DELETE
                    delete_result = supabase.table("transactions").delete().eq("id", test_id).execute()
                    print("✅ DELETE: Transação de teste removida")
                else:
                    print("❌ UPDATE: Falha ao atualizar")
            else:
                print("❌ READ: Falha ao ler")
        else:
            print("❌ CREATE: Falha ao criar transação de teste")
            
    except Exception as e:
        print(f"❌ Erro nas operações CRUD: {e}")
        return False
    
    print()
    
    # 5. Verificar estrutura da tabela
    print("5. Verificando estrutura da tabela:")
    
    try:
        # Buscar algumas transações para verificar campos
        result = supabase.table("transactions").select("*").limit(3).execute()
        
        if result.data:
            sample = result.data[0]
            required_fields = ['id', 'type', 'amount', 'description', 'created_at', 'updated_at']
            
            print("✅ Campos encontrados:")
            for field in required_fields:
                if field in sample:
                    print(f"   ✅ {field}: {type(sample[field]).__name__}")
                else:
                    print(f"   ❌ {field}: AUSENTE")
        else:
            print("ℹ️  Não há dados para verificar estrutura")
            
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")
    
    print()
    print("=" * 50)
    print("✅ Verificação concluída com sucesso!")
    print("🚀 Banco de dados configurado e funcionando")
    
    return True

if __name__ == "__main__":
    # Configurar variáveis de ambiente se não estiverem definidas
    if not os.getenv('SUPABASE_URL'):
        print("⚠️  Configure as variáveis de ambiente SUPABASE_URL e SUPABASE_ANON_KEY")
        print("Exemplo:")
        print("export SUPABASE_URL='https://seu-projeto.supabase.co'")
        print("export SUPABASE_ANON_KEY='sua-chave-anonima'")
        exit(1)
    
    success = verify_database()
    
    if success:
        print("\n🎉 Tudo funcionando! Sua API está pronta para uso.")
    else:
        print("\n🚨 Problemas encontrados. Verifique a configuração.")
        exit(1)