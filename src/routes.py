"""
Rotas da API Flask para MyFinance
Define os endpoints da aplicação
"""

from flask import Blueprint, request, jsonify, current_app
from .app import db
from .models import Transaction, Category, User
from datetime import datetime
import uuid
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Criar blueprint para a API
api_bp = Blueprint('api', __name__)

# ===============================
# DECORADORES E UTILITÁRIOS
# ===============================

def handle_errors(f):
    """Decorator para tratamento de erros padronizado"""
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': 'Dados inválidos', 'message': str(e)}), 400
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'Violação de integridade', 'message': 'Dados já existem ou são inválidos'}), 409
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {e}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error: {e}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    wrapper.__name__ = f.__name__
    return wrapper

def validate_transaction_data(data):
    """Valida dados de uma transação"""
    errors = []
    
    # Verificar campos obrigatórios
    if not data.get('type'):
        errors.append("Campo 'type' é obrigatório")
    elif data['type'] not in ['income', 'expense']:
        errors.append("Campo 'type' deve ser 'income' ou 'expense'")
    
    if not data.get('amount'):
        errors.append("Campo 'amount' é obrigatório")
    else:
        try:
            amount = Decimal(str(data['amount']))
            if amount <= 0:
                errors.append("Campo 'amount' deve ser maior que zero")
        except (InvalidOperation, TypeError):
            errors.append("Campo 'amount' deve ser um número válido")
    
    if not data.get('description'):
        errors.append("Campo 'description' é obrigatório")
    elif len(data['description'].strip()) == 0:
        errors.append("Campo 'description' não pode estar vazio")
    
    return errors

# ===============================
# ROTAS DE SAÚDE E STATUS
# ===============================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    try:
        # Testar conexão com banco
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy',
        'message': f'{current_app.config["PROJECT_NAME"]} API is running',
        'database': db_status,
        'version': '2.0.0',
        'framework': 'Flask + SQLAlchemy'
    })

@api_bp.route('/status', methods=['GET'])
@handle_errors
def get_status():
    """Retorna status detalhado da aplicação"""
    summary = Transaction.get_summary()
    
    return jsonify({
        'application': current_app.config['PROJECT_NAME'],
        'environment': current_app.config.get('ENV', 'development'),
        'database': {
            'engine': 'SQLAlchemy',
            'status': 'connected'
        },
        'statistics': summary
    })

# ===============================
# ROTAS DE TRANSAÇÕES
# ===============================

@api_bp.route('/transactions/', methods=['GET'])
@handle_errors
def list_transactions():
    """Lista todas as transações"""
    # Parâmetros de query opcional
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)  # Máximo 100
    transaction_type = request.args.get('type')
    
    # Query base
    query = Transaction.query
    
    # Filtrar por tipo se especificado
    if transaction_type in ['income', 'expense']:
        query = query.filter(Transaction.type == transaction_type)
    
    # Ordenar por data de criação (mais recentes primeiro)
    query = query.order_by(Transaction.created_at.desc())
    
    # Paginação
    transactions = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'transactions': [t.to_dict() for t in transactions.items],
        'pagination': {
            'page': transactions.page,
            'pages': transactions.pages,
            'per_page': transactions.per_page,
            'total': transactions.total,
            'has_next': transactions.has_next,
            'has_prev': transactions.has_prev
        }
    })

@api_bp.route('/transactions/', methods=['POST'])
@handle_errors
def create_transaction():
    """Cria uma nova transação"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
    
    # Validar dados
    errors = validate_transaction_data(data)
    if errors:
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Criar transação
    transaction = Transaction.create_from_dict(data)
    
    # Salvar no banco
    db.session.add(transaction)
    db.session.commit()
    
    current_app.logger.info(f"Transação criada: {transaction.id}")
    
    return jsonify(transaction.to_dict()), 201

@api_bp.route('/transactions/<transaction_id>', methods=['GET'])
@handle_errors
def get_transaction(transaction_id):
    """Busca uma transação específica"""
    try:
        transaction_uuid = uuid.UUID(transaction_id)
    except ValueError:
        return jsonify({'error': 'ID de transação inválido'}), 400
    
    transaction = Transaction.query.filter_by(id=transaction_uuid).first()
    
    if not transaction:
        return jsonify({'error': 'Transação não encontrada'}), 404
    
    return jsonify(transaction.to_dict())

@api_bp.route('/transactions/<transaction_id>', methods=['PUT'])
@handle_errors
def update_transaction(transaction_id):
    """Atualiza uma transação existente"""
    try:
        transaction_uuid = uuid.UUID(transaction_id)
    except ValueError:
        return jsonify({'error': 'ID de transação inválido'}), 400
    
    transaction = Transaction.query.filter_by(id=transaction_uuid).first()
    
    if not transaction:
        return jsonify({'error': 'Transação não encontrada'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
    
    # Validar dados
    errors = validate_transaction_data(data)
    if errors:
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Atualizar campos
    transaction.type = data['type']
    transaction.amount = Decimal(str(data['amount']))
    transaction.description = data['description']
    transaction.updated_at = datetime.utcnow()
    
    # Se houver categoria no dados, atualizar
    if 'category_id' in data and data['category_id']:
        try:
            category_uuid = uuid.UUID(data['category_id'])
            # Verificar se categoria existe
            if Category.query.filter_by(id=category_uuid).first():
                transaction.category_id = category_uuid
        except ValueError:
            return jsonify({'error': 'ID de categoria inválido'}), 400
    
    db.session.commit()
    
    current_app.logger.info(f"Transação atualizada: {transaction.id}")
    
    return jsonify(transaction.to_dict())

@api_bp.route('/transactions/<transaction_id>', methods=['DELETE'])
@handle_errors
def delete_transaction(transaction_id):
    """Deleta uma transação"""
    try:
        transaction_uuid = uuid.UUID(transaction_id)
    except ValueError:
        return jsonify({'error': 'ID de transação inválido'}), 400
    
    transaction = Transaction.query.filter_by(id=transaction_uuid).first()
    
    if not transaction:
        return jsonify({'error': 'Transação não encontrada'}), 404
    
    db.session.delete(transaction)
    db.session.commit()
    
    current_app.logger.info(f"Transação deletada: {transaction_id}")
    
    return jsonify({'message': 'Transação deletada com sucesso'}), 200

# ===============================
# ROTAS DE RESUMO E ESTATÍSTICAS
# ===============================

@api_bp.route('/summary', methods=['GET'])
@handle_errors
def get_summary():
    """Retorna resumo financeiro"""
    summary = Transaction.get_summary()
    
    return jsonify({
        'summary': summary,
        'last_updated': datetime.utcnow().isoformat()
    })

@api_bp.route('/balance', methods=['GET'])
@handle_errors
def get_balance():
    """Retorna o saldo atual"""
    balance = Transaction.get_balance()
    
    return jsonify({
        'balance': balance,
        'currency': 'BRL',
        'last_updated': datetime.utcnow().isoformat()
    })

# ===============================
# ROTAS DE CATEGORIAS (FUTURO)
# ===============================

@api_bp.route('/categories/', methods=['GET'])
@handle_errors
def list_categories():
    """Lista todas as categorias"""
    categories = Category.query.filter_by(is_active=True).all()
    
    return jsonify({
        'categories': [c.to_dict() for c in categories]
    })

@api_bp.route('/categories/', methods=['POST'])
@handle_errors
def create_category():
    """Cria uma nova categoria"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Campo name é obrigatório'}), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description', ''),
        color=data.get('color')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

# ===============================
# TRATAMENTO DE ERROS GLOBAL
# ===============================

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método não permitido'}), 405

@api_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Erro interno do servidor'}), 500