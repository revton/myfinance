import React from 'react';
// Importar apenas os ícones que usamos
import {
  Category, Home, Restaurant, Commute, ShoppingCart, 
  LocalActivity, HealthAndSafety, School, Work, 
  MonetizationOn, ShowChart, CardGiftcard, DirectionsCar, 
  Flight, DirectionsBus, DirectionsBike, Coffee, 
  LocalGroceryStore, LocalPharmacy, LocalHospital, 
  MedicalServices, FitnessCenter, SportsEsports, Movie, 
  MusicNote, Book, Luggage, Hotel, CreditCard
} from '@mui/icons-material';

// Mapear nomes de ícones para componentes
const iconMap: Record<string, React.ElementType> = {
  'category': Category,
  'home': Home,
  'restaurant': Restaurant,
  'commute': Commute,
  'shopping_cart': ShoppingCart,
  'local_activity': LocalActivity,
  'health_and_safety': HealthAndSafety,
  'school': School,
  'work': Work,
  'monetization_on': MonetizationOn,
  'show_chart': ShowChart,
  'card_giftcard': CardGiftcard,
  'directions_car': DirectionsCar,
  'flight': Flight,
  'directions_bus': DirectionsBus,
  'directions_bike': DirectionsBike,
  'coffee': Coffee,
  'local_grocery_store': LocalGroceryStore,
  'local_pharmacy': LocalPharmacy,
  'local_hospital': LocalHospital,
  'medical_services': MedicalServices,
  'fitness_center': FitnessCenter,
  'sports_esports': SportsEsports,
  'movie': Movie,
  'music_note': MusicNote,
  'book': Book,
  'luggage': Luggage,
  'hotel': Hotel,
  'credit_card': CreditCard
};

export const getIconComponent = (iconName: string): React.ElementType => {
  if (!iconName) {
    return Category;
  }
  
  // Converter snake_case para PascalCase
  const pascalCaseIconName = iconName.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join('');
  
  // Verificar se temos o ícone no nosso mapa
  if (iconMap[iconName]) {
    return iconMap[iconName];
  }
  
  if (iconMap[pascalCaseIconName]) {
    return iconMap[pascalCaseIconName];
  }
  
  // Retornar ícone padrão se não encontrado
  return Category;
};