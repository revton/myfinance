export enum CategoryType {
  EXPENSE = "expense",
  INCOME = "income",
}

export interface CategoryBase {
  name: string;
  description?: string | null;
  icon: string;
  color: string;
  type: CategoryType;
}

export interface CategoryCreate extends CategoryBase {}

export interface CategoryUpdate {
  name?: string;
  description?: string | null;
  icon?: string;
  color?: string;
  is_active?: boolean;
}

export interface Category extends CategoryBase {
  id: string;
  user_id: string;
  is_default: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
