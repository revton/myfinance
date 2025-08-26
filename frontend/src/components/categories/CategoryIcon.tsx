// src/components/categories/CategoryIcon.tsx
import React from 'react';
import { 
  Fastfood, 
  DirectionsCar, 
  ShoppingCart, 
  Favorite, 
  MoreHoriz 
} from '@mui/icons-material';

interface CategoryIconProps {
  icon: string;
  color: string;
  size: 'small' | 'medium' | 'large';
}

export const CategoryIcon: React.FC<CategoryIconProps> = ({ icon, color, size }) => {
  const icons: { [key: string]: React.ReactElement } = {
    Fastfood: <Fastfood />, 
    DirectionsCar: <DirectionsCar />, 
    ShoppingCart: <ShoppingCart />, 
    Favorite: <Favorite />, 
    MoreHoriz: <MoreHoriz />
  };

  const selectedIcon = icons[icon] || <MoreHoriz />;

  return React.cloneElement(selectedIcon, { style: { color }, fontSize: size });
};