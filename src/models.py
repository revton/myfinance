"""
Modelos SQLAlchemy para MyFinance
Define a estrutura das tabelas do banco de dados
"""

from .app import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint

class BaseModel(db.Model):
    """Modelo base com campos comuns"""
    __abstract__ = True
    
    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class Transaction(BaseModel):
    """Modelo para transações financeiras"""
    __tablename__ = 'transactions'
    
    # Campos principais
    type = db.Column(
        db.String(10),
        nullable=False,
        index=True,
        comment="Tipo da transação: 'income' ou 'expense'"
    )
    
    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        index=True,
        comment="Valor da transação em reais"
    )
    
    description = db.Column(
        db.Text,
        nullable=False,
        comment="Descrição da transação"
    )
    
    # Campos opcionais para expansões futuras
    category_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('categories.id'),
        nullable=True,
        comment="Categoria da transação (futuro)"
    )
    
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.id'),
        nullable=True,
        comment="Usuário proprietário (futuro)"
    )
    
    # Constraints de validação
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name='check_transaction_type'),
        CheckConstraint('amount > 0', name='check_positive_amount'),
        db.Index('idx_transaction_created_at', 'created_at'),
        db.Index('idx_transaction_type_amount', 'type', 'amount'),
    )
    
    def __repr__(self):
        return f'<Transaction {self.type}: R$ {self.amount} - {self.description[:30]}>'
    
    def to_dict(self):
        """Converte o modelo para dicionário (JSON serializable)"""
        return {
            'id': str(self.id),
            'type': self.type,
            'amount': float(self.amount),
            'description': self.description,
            'category_id': str(self.category_id) if self.category_id else None,
            'user_id': str(self.user_id) if self.user_id else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def create_from_dict(cls, data: dict):
        """Cria uma transação a partir de um dicionário"""
        return cls(
            type=data['type'],
            amount=data['amount'],
            description=data['description'],
            category_id=data.get('category_id'),
            user_id=data.get('user_id')
        )
    
    @classmethod
    def get_balance(cls):
        """Calcula o saldo atual (receitas - despesas)"""
        income_total = db.session.query(
            db.func.coalesce(db.func.sum(cls.amount), 0)
        ).filter(cls.type == 'income').scalar()
        
        expense_total = db.session.query(
            db.func.coalesce(db.func.sum(cls.amount), 0)
        ).filter(cls.type == 'expense').scalar()
        
        return float(income_total - expense_total)
    
    @classmethod
    def get_summary(cls):
        """Retorna um resumo financeiro"""
        income_total = db.session.query(
            db.func.coalesce(db.func.sum(cls.amount), 0)
        ).filter(cls.type == 'income').scalar()
        
        expense_total = db.session.query(
            db.func.coalesce(db.func.sum(cls.amount), 0)
        ).filter(cls.type == 'expense').scalar()
        
        total_transactions = cls.query.count()
        
        return {
            'total_transactions': total_transactions,
            'total_income': float(income_total),
            'total_expense': float(expense_total),
            'balance': float(income_total - expense_total)
        }

class Category(BaseModel):
    """Modelo para categorias de transações (futuro)"""
    __tablename__ = 'categories'
    
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
        comment="Nome da categoria"
    )
    
    description = db.Column(
        db.Text,
        nullable=True,
        comment="Descrição da categoria"
    )
    
    color = db.Column(
        db.String(7),
        nullable=True,
        comment="Cor da categoria em hexadecimal (#RRGGBB)"
    )
    
    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        comment="Se a categoria está ativa"
    )
    
    # Relacionamento com transações
    transactions = db.relationship(
        'Transaction',
        backref='category',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class User(BaseModel):
    """Modelo para usuários (futuro - autenticação)"""
    __tablename__ = 'users'
    
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="Email do usuário"
    )
    
    name = db.Column(
        db.String(255),
        nullable=False,
        comment="Nome completo do usuário"
    )
    
    password_hash = db.Column(
        db.String(255),
        nullable=True,
        comment="Hash da senha (quando não usar OAuth)"
    )
    
    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        comment="Se o usuário está ativo"
    )
    
    # Relacionamento com transações
    transactions = db.relationship(
        'Transaction',
        backref='user',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }