"""
Testes para a aplicação Flask MyFinance
Inclui testes de API, modelos e migrações
"""

import pytest
import json
import uuid
from decimal import Decimal
from src.app import create_app, db
from src.models import Transaction, Category, User

@pytest.fixture
def app():
    """Fixture para criar app Flask para testes"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture para cliente de teste"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture para runner CLI"""
    return app.test_cli_runner()

class TestHealthAndStatus:
    """Testes para endpoints de saúde e status"""
    
    def test_health_endpoint(self, client):
        """Testa endpoint de saúde"""
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'MyFinance' in data['message']
        assert data['framework'] == 'Flask + SQLAlchemy'
        assert data['version'] == '2.0.0'
    
    def test_status_endpoint(self, client):
        """Testa endpoint de status"""
        response = client.get('/api/v1/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['application'] == 'MyFinance'
        assert 'statistics' in data
        assert 'database' in data

class TestTransactionModel:
    """Testes para o modelo Transaction"""
    
    def test_create_transaction(self, app):
        """Testa criação de transação"""
        with app.app_context():
            transaction = Transaction(
                type='income',
                amount=Decimal('1500.00'),
                description='Salário de teste'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            assert transaction.id is not None
            assert transaction.type == 'income'
            assert transaction.amount == Decimal('1500.00')
            assert transaction.description == 'Salário de teste'
            assert transaction.created_at is not None
            assert transaction.updated_at is not None
    
    def test_transaction_to_dict(self, app):
        """Testa conversão de transação para dicionário"""
        with app.app_context():
            transaction = Transaction(
                type='expense',
                amount=Decimal('50.00'),
                description='Café'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            data = transaction.to_dict()
            
            assert data['type'] == 'expense'
            assert data['amount'] == 50.0
            assert data['description'] == 'Café'
            assert 'id' in data
            assert 'created_at' in data
            assert 'updated_at' in data
    
    def test_create_from_dict(self, app):
        """Testa criação de transação a partir de dicionário"""
        with app.app_context():
            data = {
                'type': 'income',
                'amount': 2000.00,
                'description': 'Freelance'
            }
            
            transaction = Transaction.create_from_dict(data)
            
            assert transaction.type == 'income'
            assert transaction.amount == Decimal('2000.00')
            assert transaction.description == 'Freelance'
    
    def test_get_balance(self, app):
        """Testa cálculo de saldo"""
        with app.app_context():
            # Criar receitas
            income1 = Transaction(type='income', amount=Decimal('1000.00'), description='Receita 1')
            income2 = Transaction(type='income', amount=Decimal('500.00'), description='Receita 2')
            
            # Criar despesas
            expense1 = Transaction(type='expense', amount=Decimal('300.00'), description='Despesa 1')
            expense2 = Transaction(type='expense', amount=Decimal('200.00'), description='Despesa 2')
            
            db.session.add_all([income1, income2, expense1, expense2])
            db.session.commit()
            
            balance = Transaction.get_balance()
            expected_balance = 1000.00 + 500.00 - 300.00 - 200.00  # 1000.00
            
            assert balance == expected_balance
    
    def test_get_summary(self, app):
        """Testa resumo financeiro"""
        with app.app_context():
            # Criar transações
            income = Transaction(type='income', amount=Decimal('1000.00'), description='Receita')
            expense = Transaction(type='expense', amount=Decimal('400.00'), description='Despesa')
            
            db.session.add_all([income, expense])
            db.session.commit()
            
            summary = Transaction.get_summary()
            
            assert summary['total_transactions'] == 2
            assert summary['total_income'] == 1000.0
            assert summary['total_expense'] == 400.0
            assert summary['balance'] == 600.0

class TestTransactionAPI:
    """Testes para API de transações"""
    
    def test_list_empty_transactions(self, client):
        """Testa listagem de transações vazia"""
        response = client.get('/api/v1/transactions/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['transactions'] == []
        assert 'pagination' in data
    
    def test_create_transaction_success(self, client):
        """Testa criação de transação com sucesso"""
        transaction_data = {
            'type': 'income',
            'amount': 1500.50,
            'description': 'Salário Janeiro'
        }
        
        response = client.post(
            '/api/v1/transactions/',
            data=json.dumps(transaction_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['type'] == 'income'
        assert data['amount'] == 1500.5
        assert data['description'] == 'Salário Janeiro'
        assert 'id' in data
    
    def test_create_transaction_validation_errors(self, client):
        """Testa validação na criação de transação"""
        # Teste sem dados
        response = client.post('/api/v1/transactions/')
        assert response.status_code == 400
        
        # Teste com dados inválidos
        invalid_data = {
            'type': 'invalid_type',
            'amount': -100,
            'description': ''
        }
        
        response = client.post(
            '/api/v1/transactions/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'details' in data
    
    def test_get_transaction_by_id(self, client, app):
        """Testa busca de transação por ID"""
        with app.app_context():
            transaction = Transaction(
                type='expense',
                amount=Decimal('75.00'),
                description='Combustível'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            transaction_id = str(transaction.id)
        
        response = client.get(f'/api/v1/transactions/{transaction_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['type'] == 'expense'
        assert data['amount'] == 75.0
        assert data['description'] == 'Combustível'
    
    def test_get_transaction_not_found(self, client):
        """Testa busca de transação não encontrada"""
        fake_id = str(uuid.uuid4())
        response = client.get(f'/api/v1/transactions/{fake_id}')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_transaction(self, client, app):
        """Testa atualização de transação"""
        with app.app_context():
            transaction = Transaction(
                type='expense',
                amount=Decimal('100.00'),
                description='Supermercado original'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            transaction_id = str(transaction.id)
        
        update_data = {
            'type': 'expense',
            'amount': 120.00,
            'description': 'Supermercado atualizado'
        }
        
        response = client.put(
            f'/api/v1/transactions/{transaction_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['amount'] == 120.0
        assert data['description'] == 'Supermercado atualizado'
    
    def test_delete_transaction(self, client, app):
        """Testa exclusão de transação"""
        with app.app_context():
            transaction = Transaction(
                type='expense',
                amount=Decimal('50.00'),
                description='Para deletar'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            transaction_id = str(transaction.id)
        
        response = client.delete(f'/api/v1/transactions/{transaction_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verificar se foi realmente deletado
        response = client.get(f'/api/v1/transactions/{transaction_id}')
        assert response.status_code == 404
    
    def test_list_transactions_with_pagination(self, client, app):
        """Testa listagem com paginação"""
        with app.app_context():
            # Criar várias transações
            for i in range(15):
                transaction = Transaction(
                    type='income' if i % 2 == 0 else 'expense',
                    amount=Decimal(f'{100 + i}.00'),
                    description=f'Transação {i}'
                )
                db.session.add(transaction)
            
            db.session.commit()
        
        # Testar primeira página
        response = client.get('/api/v1/transactions/?page=1&per_page=10')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['transactions']) == 10
        assert data['pagination']['page'] == 1
        assert data['pagination']['total'] == 15
        assert data['pagination']['has_next'] is True
    
    def test_list_transactions_filter_by_type(self, client, app):
        """Testa filtro por tipo de transação"""
        with app.app_context():
            income = Transaction(type='income', amount=Decimal('1000.00'), description='Receita')
            expense = Transaction(type='expense', amount=Decimal('500.00'), description='Despesa')
            
            db.session.add_all([income, expense])
            db.session.commit()
        
        # Filtrar apenas receitas
        response = client.get('/api/v1/transactions/?type=income')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['transactions']) == 1
        assert data['transactions'][0]['type'] == 'income'

class TestSummaryAPI:
    """Testes para endpoints de resumo"""
    
    def test_get_summary(self, client, app):
        """Testa endpoint de resumo"""
        with app.app_context():
            income = Transaction(type='income', amount=Decimal('2000.00'), description='Receita')
            expense = Transaction(type='expense', amount=Decimal('800.00'), description='Despesa')
            
            db.session.add_all([income, expense])
            db.session.commit()
        
        response = client.get('/api/v1/summary')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['summary']['total_income'] == 2000.0
        assert data['summary']['total_expense'] == 800.0
        assert data['summary']['balance'] == 1200.0
        assert 'last_updated' in data
    
    def test_get_balance(self, client, app):
        """Testa endpoint de saldo"""
        with app.app_context():
            income = Transaction(type='income', amount=Decimal('1500.00'), description='Receita')
            expense = Transaction(type='expense', amount=Decimal('600.00'), description='Despesa')
            
            db.session.add_all([income, expense])
            db.session.commit()
        
        response = client.get('/api/v1/balance')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['balance'] == 900.0
        assert data['currency'] == 'BRL'
        assert 'last_updated' in data

class TestCLICommands:
    """Testes para comandos CLI"""
    
    def test_init_db_command(self, runner):
        """Testa comando de inicialização do banco"""
        result = runner.invoke(args=['init_db'])
        assert result.exit_code == 0
        assert 'inicializado com sucesso' in result.output
    
    def test_status_command(self, runner, app):
        """Testa comando de status"""
        with app.app_context():
            # Criar algumas transações
            income = Transaction(type='income', amount=Decimal('1000.00'), description='Teste')
            db.session.add(income)
            db.session.commit()
        
        result = runner.invoke(args=['status'])
        assert result.exit_code == 0
        assert 'MyFinance' in result.output
        assert 'Total de transações: 1' in result.output