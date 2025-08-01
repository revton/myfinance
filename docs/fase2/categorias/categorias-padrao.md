# 🏷️ Categorias Padrão - Sistema de Categorias

## 🎯 **Visão Geral**

Este documento define as categorias padrão que serão criadas automaticamente para todos os usuários, fornecendo uma base sólida para organização financeira.

## 📋 **Categorias de Despesas**

### **1. Alimentação**
- **Nome**: Alimentação
- **Descrição**: Gastos com comida e bebida
- **Ícone**: food
- **Cor**: #FF6B6B
- **Subcategorias Sugeridas**:
  - Supermercado
  - Restaurante
  - Delivery
  - Cafés e lanches

### **2. Transporte**
- **Nome**: Transporte
- **Descrição**: Combustível, transporte público, táxi
- **Ícone**: transport
- **Cor**: #4ECDC4
- **Subcategorias Sugeridas**:
  - Combustível
  - Transporte público
  - Táxi/Uber
  - Manutenção do carro

### **3. Moradia**
- **Nome**: Moradia
- **Descrição**: Aluguel, contas de casa, manutenção
- **Ícone**: home
- **Cor**: #45B7D1
- **Subcategorias Sugeridas**:
  - Aluguel
  - Contas (luz, água, gás)
  - Internet/Telefone
  - Manutenção

### **4. Saúde**
- **Nome**: Saúde
- **Descrição**: Médico, farmácia, plano de saúde
- **Ícone**: health
- **Cor**: #96CEB4
- **Subcategorias Sugeridas**:
  - Consultas médicas
  - Farmácia
  - Plano de saúde
  - Exames

### **5. Educação**
- **Nome**: Educação
- **Descrição**: Cursos, livros, material escolar
- **Ícone**: education
- **Cor**: #FFEAA7
- **Subcategorias Sugeridas**:
  - Cursos
  - Livros
  - Material escolar
  - Mensalidades

### **6. Entretenimento**
- **Nome**: Entretenimento
- **Descrição**: Cinema, shows, hobbies
- **Ícone**: entertainment
- **Cor**: #DDA0DD
- **Subcategorias Sugeridas**:
  - Cinema/Teatro
  - Shows/Concertos
  - Hobbies
  - Jogos

### **7. Compras**
- **Nome**: Compras
- **Descrição**: Roupas, eletrônicos, outros
- **Ícone**: shopping
- **Cor**: #FFB347
- **Subcategorias Sugeridas**:
  - Roupas
  - Eletrônicos
  - Acessórios
  - Presentes

### **8. Restaurante**
- **Nome**: Restaurante
- **Descrição**: Refeições fora de casa
- **Ícone**: restaurant
- **Cor**: #FF8C69
- **Subcategorias Sugeridas**:
  - Almoço
  - Jantar
  - Delivery
  - Fast food

### **9. Viagem**
- **Nome**: Viagem
- **Descrição**: Passagens, hospedagem, turismo
- **Ícone**: travel
- **Cor**: #87CEEB
- **Subcategorias Sugeridas**:
  - Passagens
  - Hospedagem
  - Alimentação em viagem
  - Passeios

### **10. Outros**
- **Nome**: Outros
- **Descrição**: Despesas diversas
- **Ícone**: category
- **Cor**: #C0C0C0
- **Subcategorias Sugeridas**:
  - Despesas inesperadas
  - Multas
  - Doações
  - Outros

## 💰 **Categorias de Receitas**

### **1. Salário**
- **Nome**: Salário
- **Descrição**: Rendimento do trabalho principal
- **Ícone**: work
- **Cor**: #32CD32
- **Subcategorias Sugeridas**:
  - Salário fixo
  - Comissões
  - Bônus
  - 13º salário

### **2. Freelance**
- **Nome**: Freelance
- **Descrição**: Trabalhos extras e projetos
- **Ícone**: work
- **Cor**: #228B22
- **Subcategorias Sugeridas**:
  - Projetos freelance
  - Consultorias
  - Aulas particulares
  - Trabalhos pontuais

### **3. Investimentos**
- **Nome**: Investimentos
- **Descrição**: Rendimentos de aplicações
- **Ícone**: investment
- **Cor**: #FFD700
- **Subcategorias Sugeridas**:
  - Renda fixa
  - Ações
  - Fundos imobiliários
  - Criptomoedas

### **4. Presentes**
- **Nome**: Presentes
- **Descrição**: Dinheiro recebido como presente
- **Ícone**: gift
- **Cor**: #FF69B4
- **Subcategorias Sugeridas**:
  - Aniversário
  - Natal
  - Casamento
  - Outros eventos

### **5. Reembolso**
- **Nome**: Reembolso
- **Descrição**: Valores reembolsados
- **Ícone**: cash
- **Cor**: #90EE90
- **Subcategorias Sugeridas**:
  - Reembolso de despesas
  - Devoluções
  - Restituições
  - Seguros

### **6. Outros**
- **Nome**: Outros
- **Descrição**: Receitas diversas
- **Ícone**: category
- **Cor**: #98FB98
- **Subcategorias Sugeridas**:
  - Vendas
  - Aluguel recebido
  - Heranças
  - Outros

## 🔧 **Implementação Técnica**

### **Script SQL para Criação das Categorias Padrão**

```sql
-- Função para criar categorias padrão para um usuário
CREATE OR REPLACE FUNCTION create_default_categories(user_uuid UUID)
RETURNS VOID AS $$
BEGIN
    -- Categorias de Despesas
    INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
    (user_uuid, 'Alimentação', 'Gastos com comida e bebida', 'food', '#FF6B6B', 'expense', TRUE),
    (user_uuid, 'Transporte', 'Combustível, transporte público, táxi', 'transport', '#4ECDC4', 'expense', TRUE),
    (user_uuid, 'Moradia', 'Aluguel, contas de casa, manutenção', 'home', '#45B7D1', 'expense', TRUE),
    (user_uuid, 'Saúde', 'Médico, farmácia, plano de saúde', 'health', '#96CEB4', 'expense', TRUE),
    (user_uuid, 'Educação', 'Cursos, livros, material escolar', 'education', '#FFEAA7', 'expense', TRUE),
    (user_uuid, 'Entretenimento', 'Cinema, shows, hobbies', 'entertainment', '#DDA0DD', 'expense', TRUE),
    (user_uuid, 'Compras', 'Roupas, eletrônicos, outros', 'shopping', '#FFB347', 'expense', TRUE),
    (user_uuid, 'Restaurante', 'Refeições fora de casa', 'restaurant', '#FF8C69', 'expense', TRUE),
    (user_uuid, 'Viagem', 'Passagens, hospedagem, turismo', 'travel', '#87CEEB', 'expense', TRUE),
    (user_uuid, 'Outros', 'Despesas diversas', 'category', '#C0C0C0', 'expense', TRUE);

    -- Categorias de Receitas
    INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
    (user_uuid, 'Salário', 'Rendimento do trabalho principal', 'work', '#32CD32', 'income', TRUE),
    (user_uuid, 'Freelance', 'Trabalhos extras e projetos', 'work', '#228B22', 'income', TRUE),
    (user_uuid, 'Investimentos', 'Rendimentos de aplicações', 'investment', '#FFD700', 'income', TRUE),
    (user_uuid, 'Presentes', 'Dinheiro recebido como presente', 'gift', '#FF69B4', 'income', TRUE),
    (user_uuid, 'Reembolso', 'Valores reembolsados', 'cash', '#90EE90', 'income', TRUE),
    (user_uuid, 'Outros', 'Receitas diversas', 'category', '#98FB98', 'income', TRUE);
END;
$$ LANGUAGE plpgsql;

-- Trigger para criar categorias padrão quando um novo usuário é registrado
CREATE OR REPLACE FUNCTION trigger_create_default_categories()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se é um novo usuário
    IF TG_OP = 'INSERT' THEN
        -- Criar categorias padrão para o novo usuário
        PERFORM create_default_categories(NEW.id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar trigger na tabela auth.users
CREATE TRIGGER create_default_categories_trigger
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION trigger_create_default_categories();
```

### **Implementação em Python (Alembic Migration)**

```python
# migrations/versions/0004_create_default_categories.py
"""Create default categories

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Criar função para criar categorias padrão
    op.execute("""
        CREATE OR REPLACE FUNCTION create_default_categories(user_uuid UUID)
        RETURNS VOID AS $$
        BEGIN
            -- Categorias de Despesas
            INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
            (user_uuid, 'Alimentação', 'Gastos com comida e bebida', 'food', '#FF6B6B', 'expense', TRUE),
            (user_uuid, 'Transporte', 'Combustível, transporte público, táxi', 'transport', '#4ECDC4', 'expense', TRUE),
            (user_uuid, 'Moradia', 'Aluguel, contas de casa, manutenção', 'home', '#45B7D1', 'expense', TRUE),
            (user_uuid, 'Saúde', 'Médico, farmácia, plano de saúde', 'health', '#96CEB4', 'expense', TRUE),
            (user_uuid, 'Educação', 'Cursos, livros, material escolar', 'education', '#FFEAA7', 'expense', TRUE),
            (user_uuid, 'Entretenimento', 'Cinema, shows, hobbies', 'entertainment', '#DDA0DD', 'expense', TRUE),
            (user_uuid, 'Compras', 'Roupas, eletrônicos, outros', 'shopping', '#FFB347', 'expense', TRUE),
            (user_uuid, 'Restaurante', 'Refeições fora de casa', 'restaurant', '#FF8C69', 'expense', TRUE),
            (user_uuid, 'Viagem', 'Passagens, hospedagem, turismo', 'travel', '#87CEEB', 'expense', TRUE),
            (user_uuid, 'Outros', 'Despesas diversas', 'category', '#C0C0C0', 'expense', TRUE);

            -- Categorias de Receitas
            INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
            (user_uuid, 'Salário', 'Rendimento do trabalho principal', 'work', '#32CD32', 'income', TRUE),
            (user_uuid, 'Freelance', 'Trabalhos extras e projetos', 'work', '#228B22', 'income', TRUE),
            (user_uuid, 'Investimentos', 'Rendimentos de aplicações', 'investment', '#FFD700', 'income', TRUE),
            (user_uuid, 'Presentes', 'Dinheiro recebido como presente', 'gift', '#FF69B4', 'income', TRUE),
            (user_uuid, 'Reembolso', 'Valores reembolsados', 'cash', '#90EE90', 'income', TRUE),
            (user_uuid, 'Outros', 'Receitas diversas', 'category', '#98FB98', 'income', TRUE);
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover função
    op.execute("DROP FUNCTION IF EXISTS create_default_categories(UUID)")
```

### **Serviço Python para Gerenciamento**

```python
# app/services/category_service.py
from typing import List, Optional
from uuid import UUID
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.database import get_supabase_client

class CategoryService:
    def __init__(self):
        self.supabase = get_supabase_client()

    async def create_default_categories(self, user_id: UUID) -> List[Category]:
        """Cria categorias padrão para um usuário"""
        default_categories = [
            # Despesas
            CategoryCreate(
                name="Alimentação",
                description="Gastos com comida e bebida",
                icon="food",
                color="#FF6B6B",
                type="expense"
            ),
            CategoryCreate(
                name="Transporte",
                description="Combustível, transporte público, táxi",
                icon="transport",
                color="#4ECDC4",
                type="expense"
            ),
            CategoryCreate(
                name="Moradia",
                description="Aluguel, contas de casa, manutenção",
                icon="home",
                color="#45B7D1",
                type="expense"
            ),
            CategoryCreate(
                name="Saúde",
                description="Médico, farmácia, plano de saúde",
                icon="health",
                color="#96CEB4",
                type="expense"
            ),
            CategoryCreate(
                name="Educação",
                description="Cursos, livros, material escolar",
                icon="education",
                color="#FFEAA7",
                type="expense"
            ),
            CategoryCreate(
                name="Entretenimento",
                description="Cinema, shows, hobbies",
                icon="entertainment",
                color="#DDA0DD",
                type="expense"
            ),
            CategoryCreate(
                name="Compras",
                description="Roupas, eletrônicos, outros",
                icon="shopping",
                color="#FFB347",
                type="expense"
            ),
            CategoryCreate(
                name="Restaurante",
                description="Refeições fora de casa",
                icon="restaurant",
                color="#FF8C69",
                type="expense"
            ),
            CategoryCreate(
                name="Viagem",
                description="Passagens, hospedagem, turismo",
                icon="travel",
                color="#87CEEB",
                type="expense"
            ),
            CategoryCreate(
                name="Outros",
                description="Despesas diversas",
                icon="category",
                color="#C0C0C0",
                type="expense"
            ),
            # Receitas
            CategoryCreate(
                name="Salário",
                description="Rendimento do trabalho principal",
                icon="work",
                color="#32CD32",
                type="income"
            ),
            CategoryCreate(
                name="Freelance",
                description="Trabalhos extras e projetos",
                icon="work",
                color="#228B22",
                type="income"
            ),
            CategoryCreate(
                name="Investimentos",
                description="Rendimentos de aplicações",
                icon="investment",
                color="#FFD700",
                type="income"
            ),
            CategoryCreate(
                name="Presentes",
                description="Dinheiro recebido como presente",
                icon="gift",
                color="#FF69B4",
                type="income"
            ),
            CategoryCreate(
                name="Reembolso",
                description="Valores reembolsados",
                icon="cash",
                color="#90EE90",
                type="income"
            ),
            CategoryCreate(
                name="Outros",
                description="Receitas diversas",
                icon="category",
                color="#98FB98",
                type="income"
            )
        ]

        created_categories = []
        for category_data in default_categories:
            category_data.user_id = user_id
            category_data.is_default = True
            
            result = await self.create_category(category_data)
            created_categories.append(result)

        return created_categories

    async def create_category(self, category_data: CategoryCreate) -> Category:
        """Cria uma nova categoria"""
        data = category_data.dict()
        
        result = self.supabase.table('categories').insert(data).execute()
        
        if result.error:
            raise Exception(f"Erro ao criar categoria: {result.error}")
        
        return Category(**result.data[0])

    async def get_categories_by_user(self, user_id: UUID, include_default: bool = True) -> List[Category]:
        """Busca categorias de um usuário"""
        query = self.supabase.table('categories').select('*').eq('user_id', str(user_id))
        
        if not include_default:
            query = query.eq('is_default', False)
        
        result = query.execute()
        
        if result.error:
            raise Exception(f"Erro ao buscar categorias: {result.error}")
        
        return [Category(**category) for category in result.data]

    async def get_default_categories(self) -> List[Category]:
        """Busca categorias padrão do sistema"""
        result = self.supabase.table('categories').select('*').eq('is_default', True).execute()
        
        if result.error:
            raise Exception(f"Erro ao buscar categorias padrão: {result.error}")
        
        return [Category(**category) for category in result.data]
```

## 🎨 **Configuração Visual**

### **Cores e Ícones Padrão**

```typescript
// src/constants/defaultCategories.ts
export const DEFAULT_CATEGORIES = {
  expense: [
    {
      name: 'Alimentação',
      description: 'Gastos com comida e bebida',
      icon: 'food',
      color: '#FF6B6B',
      type: 'expense' as const
    },
    {
      name: 'Transporte',
      description: 'Combustível, transporte público, táxi',
      icon: 'transport',
      color: '#4ECDC4',
      type: 'expense' as const
    },
    {
      name: 'Moradia',
      description: 'Aluguel, contas de casa, manutenção',
      icon: 'home',
      color: '#45B7D1',
      type: 'expense' as const
    },
    {
      name: 'Saúde',
      description: 'Médico, farmácia, plano de saúde',
      icon: 'health',
      color: '#96CEB4',
      type: 'expense' as const
    },
    {
      name: 'Educação',
      description: 'Cursos, livros, material escolar',
      icon: 'education',
      color: '#FFEAA7',
      type: 'expense' as const
    },
    {
      name: 'Entretenimento',
      description: 'Cinema, shows, hobbies',
      icon: 'entertainment',
      color: '#DDA0DD',
      type: 'expense' as const
    },
    {
      name: 'Compras',
      description: 'Roupas, eletrônicos, outros',
      icon: 'shopping',
      color: '#FFB347',
      type: 'expense' as const
    },
    {
      name: 'Restaurante',
      description: 'Refeições fora de casa',
      icon: 'restaurant',
      color: '#FF8C69',
      type: 'expense' as const
    },
    {
      name: 'Viagem',
      description: 'Passagens, hospedagem, turismo',
      icon: 'travel',
      color: '#87CEEB',
      type: 'expense' as const
    },
    {
      name: 'Outros',
      description: 'Despesas diversas',
      icon: 'category',
      color: '#C0C0C0',
      type: 'expense' as const
    }
  ],
  income: [
    {
      name: 'Salário',
      description: 'Rendimento do trabalho principal',
      icon: 'work',
      color: '#32CD32',
      type: 'income' as const
    },
    {
      name: 'Freelance',
      description: 'Trabalhos extras e projetos',
      icon: 'work',
      color: '#228B22',
      type: 'income' as const
    },
    {
      name: 'Investimentos',
      description: 'Rendimentos de aplicações',
      icon: 'investment',
      color: '#FFD700',
      type: 'income' as const
    },
    {
      name: 'Presentes',
      description: 'Dinheiro recebido como presente',
      icon: 'gift',
      color: '#FF69B4',
      type: 'income' as const
    },
    {
      name: 'Reembolso',
      description: 'Valores reembolsados',
      icon: 'cash',
      color: '#90EE90',
      type: 'income' as const
    },
    {
      name: 'Outros',
      description: 'Receitas diversas',
      icon: 'category',
      color: '#98FB98',
      type: 'income' as const
    }
  ]
};

export const getDefaultCategoriesByType = (type: 'expense' | 'income') => {
  return DEFAULT_CATEGORIES[type];
};

export const getAllDefaultCategories = () => {
  return [...DEFAULT_CATEGORIES.expense, ...DEFAULT_CATEGORIES.income];
};
```

### **Hook para Gerenciamento de Categorias Padrão**

```typescript
// src/hooks/useDefaultCategories.ts
import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { Category } from '../types/category';
import { DEFAULT_CATEGORIES } from '../constants/defaultCategories';

export const useDefaultCategories = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const createDefaultCategories = async (userId: string) => {
    try {
      setLoading(true);
      setError(null);

      const allCategories = [
        ...DEFAULT_CATEGORIES.expense,
        ...DEFAULT_CATEGORIES.income
      ];

      const categoriesToInsert = allCategories.map(category => ({
        ...category,
        user_id: userId,
        is_default: true
      }));

      const { data, error: insertError } = await supabase
        .from('categories')
        .insert(categoriesToInsert)
        .select();

      if (insertError) throw insertError;

      return data;
    } catch (err) {
      setError('Erro ao criar categorias padrão');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getDefaultCategories = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('categories')
        .select('*')
        .eq('is_default', true)
        .order('name');

      if (fetchError) throw fetchError;

      return data;
    } catch (err) {
      setError('Erro ao buscar categorias padrão');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    createDefaultCategories,
    getDefaultCategories
  };
};
```

## 🔄 **Integração com Registro de Usuário**

### **Atualização do AuthService**

```typescript
// src/services/authService.ts
import { supabase } from '../lib/supabase';
import { createDefaultCategories } from '../hooks/useDefaultCategories';

export const authService = {
  // ... outros métodos ...

  async register(email: string, password: string, fullName?: string) {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName
          }
        }
      });

      if (error) throw error;

      // Se o registro foi bem-sucedido e temos um usuário
      if (data.user) {
        // Criar perfil do usuário
        const { error: profileError } = await supabase
          .from('user_profiles')
          .insert([
            {
              user_id: data.user.id,
              email: data.user.email,
              full_name: fullName
            }
          ]);

        if (profileError) throw profileError;

        // Criar categorias padrão
        await createDefaultCategories(data.user.id);
      }

      return data;
    } catch (error) {
      console.error('Erro no registro:', error);
      throw error;
    }
  }
};
```

## 📊 **Estatísticas das Categorias Padrão**

### **Métricas de Uso**

```sql
-- Consulta para estatísticas de uso das categorias padrão
SELECT 
    c.name,
    c.type,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(t.amount), 0) as total_amount,
    AVG(t.amount) as average_amount
FROM categories c
LEFT JOIN transactions t ON c.id = t.category_id
WHERE c.is_default = TRUE
    AND t.user_id = auth.uid()
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY c.id, c.name, c.type
ORDER BY total_amount DESC;
```

### **Relatório de Categorias Mais Utilizadas**

```typescript
// src/utils/categoryAnalytics.ts
export const getCategoryUsageStats = (categories: Category[], transactions: Transaction[]) => {
  const stats = categories.map(category => {
    const categoryTransactions = transactions.filter(t => t.category_id === category.id);
    const totalAmount = categoryTransactions.reduce((sum, t) => sum + Number(t.amount), 0);
    const transactionCount = categoryTransactions.length;
    const averageAmount = transactionCount > 0 ? totalAmount / transactionCount : 0;

    return {
      category,
      transactionCount,
      totalAmount,
      averageAmount,
      percentage: 0 // Será calculado depois
    };
  });

  const totalAmount = stats.reduce((sum, stat) => sum + stat.totalAmount, 0);
  
  return stats.map(stat => ({
    ...stat,
    percentage: totalAmount > 0 ? (stat.totalAmount / totalAmount) * 100 : 0
  })).sort((a, b) => b.totalAmount - a.totalAmount);
};
```

## 🧪 **Testes das Categorias Padrão**

### **Teste de Criação**

```typescript
// src/tests/defaultCategories.test.ts
import { createDefaultCategories } from '../hooks/useDefaultCategories';
import { supabase } from '../lib/supabase';

describe('Default Categories', () => {
  test('should create default categories for new user', async () => {
    const mockUserId = 'test-user-123';
    
    // Mock do Supabase
    const mockInsert = jest.fn().mockResolvedValue({
      data: [
        { id: '1', name: 'Alimentação', type: 'expense' },
        { id: '2', name: 'Salário', type: 'income' }
      ],
      error: null
    });

    (supabase.table as jest.Mock).mockReturnValue({
      insert: mockInsert
    });

    const result = await createDefaultCategories(mockUserId);

    expect(result).toHaveLength(16); // 10 despesas + 6 receitas
    expect(mockInsert).toHaveBeenCalledWith(
      expect.arrayContaining([
        expect.objectContaining({
          name: 'Alimentação',
          type: 'expense',
          is_default: true
        }),
        expect.objectContaining({
          name: 'Salário',
          type: 'income',
          is_default: true
        })
      ])
    );
  });
});
```

Esta configuração de categorias padrão garante que todos os usuários tenham uma base sólida para organizar suas finanças desde o primeiro acesso ao sistema. 