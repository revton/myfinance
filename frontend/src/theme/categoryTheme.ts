export const categoryColors = {
  expense: {
    primary: '#FF6B6B',
    secondary: '#FF8C69',
    light: '#FFB3B3',
    dark: '#E53E3E'
  },
  income: {
    primary: '#32CD32',
    secondary: '#228B22',
    light: '#90EE90',
    dark: '#228B22'
  }
};

export const categoryIcons = {
  expense: [
    'home', 'food', 'transport', 'shopping', 'entertainment',
    'health', 'education', 'restaurant', 'travel', 'car',
    'plane', 'train', 'bus', 'bike', 'coffee', 'beer',
    'wine', 'pizza', 'burger', 'sushi', 'grocery',
    'pharmacy', 'hospital', 'doctor', 'gym', 'sports',
    'movie', 'music', 'book', 'game', 'hotel', 'beach'
  ],
  income: [
    'work', 'salary', 'investment', 'gift', 'cash',
    'bank', 'wallet', 'credit_card', 'shopping_cart'
  ]
};

export const getCategoryIconColor = (type: 'expense' | 'income') => {
  return categoryColors[type].primary;
};
