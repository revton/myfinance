#!/usr/bin/env python3
"""
Script para testar a migração para SQLAlchemy direto
Testa a nova implementação da API FastAPI usando SQLAlchemy
"""

import requests
import json
import time
import sys
import os

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get("http://localhost:8002/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data}")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_create_transaction():
    """Testa criação de transação"""
    print("\n🔍 Testando criação de transação...")
    try:
        transaction_data = {
            "type": "income",
            "amount": 1000.50,
            "description": "Salário mensal"
        }
        
        response = requests.post(
            "http://localhost:8002/transactions/",
            json=transaction_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Transação criada: {data}")
            return data["id"]
        else:
            print(f"❌ Erro ao criar transação: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na criação: {e}")
        return None

def test_list_transactions():
    """Testa listagem de transações"""
    print("\n🔍 Testando listagem de transações...")
    try:
        response = requests.get("http://localhost:8002/transactions/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Transações listadas: {len(data)} encontradas")
            for t in data:
                print(f"  - {t['id']}: {t['type']} - R$ {t['amount']} - {t['description']}")
            return True
        else:
            print(f"❌ Erro ao listar transações: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na listagem: {e}")
        return False

def test_get_transaction(transaction_id):
    """Testa busca de transação específica"""
    print(f"\n🔍 Testando busca da transação {transaction_id}...")
    try:
        response = requests.get(f"http://localhost:8002/transactions/{transaction_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Transação encontrada: {data}")
            return True
        else:
            print(f"❌ Erro ao buscar transação: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return False

def test_update_transaction(transaction_id):
    """Testa atualização de transação"""
    print(f"\n🔍 Testando atualização da transação {transaction_id}...")
    try:
        update_data = {
            "amount": 1200.75,
            "description": "Salário mensal atualizado"
        }
        
        response = requests.put(
            f"http://localhost:8002/transactions/{transaction_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Transação atualizada: {data}")
            return True
        else:
            print(f"❌ Erro ao atualizar transação: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na atualização: {e}")
        return False

def test_delete_transaction(transaction_id):
    """Testa exclusão de transação"""
    print(f"\n🔍 Testando exclusão da transação {transaction_id}...")
    try:
        response = requests.delete(f"http://localhost:8002/transactions/{transaction_id}")
        
        if response.status_code == 204:
            print(f"✅ Transação deletada com sucesso")
            return True
        else:
            print(f"❌ Erro ao deletar transação: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na exclusão: {e}")
        return False

def test_invalid_transaction():
    """Testa validação de dados inválidos"""
    print("\n🔍 Testando validação de dados inválidos...")
    try:
        # Testa valor negativo
        invalid_data = {
            "type": "expense",
            "amount": -100,
            "description": "Valor negativo"
        }
        
        response = requests.post(
            "http://localhost:8002/transactions/",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:
            print(f"✅ Validação funcionando: {response.status_code}")
            return True
        else:
            print(f"❌ Validação não funcionou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de validação: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da migração para SQLAlchemy...")
    print("=" * 60)
    
    # Lista de testes
    tests = [
        ("Health Check", test_health_check),
        ("Criar Transação", test_create_transaction),
        ("Listar Transações", test_list_transactions),
        ("Buscar Transação", lambda: test_get_transaction(transaction_id) if 'transaction_id' in locals() else None),
        ("Atualizar Transação", lambda: test_update_transaction(transaction_id) if 'transaction_id' in locals() else None),
        ("Deletar Transação", lambda: test_delete_transaction(transaction_id) if 'transaction_id' in locals() else None),
        ("Validação de Dados", test_invalid_transaction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        if test_name == "Criar Transação":
            result = test_func()
            if result:
                transaction_id = result
                results.append((test_name, True))
            else:
                results.append((test_name, False))
        elif test_name in ["Buscar Transação", "Atualizar Transação", "Deletar Transação"]:
            if 'transaction_id' in locals():
                result = test_func()
                results.append((test_name, result))
            else:
                print("⚠️  Pulando teste - transação não foi criada")
                results.append((test_name, False))
        else:
            result = test_func()
            results.append((test_name, result))
        
        time.sleep(0.5)  # Pequena pausa entre testes
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Migração para SQLAlchemy bem-sucedida!")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 