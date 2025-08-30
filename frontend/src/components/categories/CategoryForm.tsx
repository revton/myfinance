import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Grid,
  FormHelperText,
  Typography,
  Tooltip,
  IconButton
} from '@mui/material';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { getIconComponent } from '../../utils/iconUtils';
import { CategoryType } from '../../types/category';

// Importar os mesmos ícones que usamos no iconUtils
import {
  Category, Home, Restaurant, Commute, ShoppingCart, 
  LocalActivity, HealthAndSafety, School, Work, 
  MonetizationOn, ShowChart, CardGiftcard, DirectionsCar, 
  Flight, DirectionsBus, DirectionsBike, Coffee, 
  LocalGroceryStore, LocalPharmacy, LocalHospital, 
  MedicalServices, FitnessCenter, SportsEsports, Movie, 
  MusicNote, Book, Luggage, Hotel, CreditCard
} from '@mui/icons-material';

interface CategoryFormProps {
  category?: Category | null;
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

const CategoryForm: React.FC<CategoryFormProps> = ({ category, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    icon: 'category',
    color: '#1976d2',
    type: CategoryType.EXPENSE
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (category) {
      setFormData({
        name: category.name,
        description: category.description || '',
        icon: category.icon,
        color: category.color,
        type: category.type
      });
    }
  }, [category]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    } else if (formData.name.length > 50) {
      newErrors.name = 'Nome deve ter no máximo 50 caracteres';
    }

    if (formData.description && formData.description.length > 200) {
      newErrors.description = 'Descrição deve ter no máximo 200 caracteres';
    }

    if (!/^#[0-9A-Fa-f]{6}$/.test(formData.color)) {
      newErrors.color = 'Cor deve estar no formato hexadecimal (#RRGGBB)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Usar os mesmos ícones disponíveis no iconUtils
  const iconOptions = [
    { value: 'category', label: 'Categoria Padrão', icon: Category },
    { value: 'home', label: 'Casa', icon: Home },
    { value: 'restaurant', label: 'Comida', icon: Restaurant },
    { value: 'commute', label: 'Transporte', icon: Commute },
    { value: 'shopping_cart', label: 'Compras', icon: ShoppingCart },
    { value: 'local_activity', label: 'Entretenimento', icon: LocalActivity },
    { value: 'health_and_safety', label: 'Saúde', icon: HealthAndSafety },
    { value: 'school', label: 'Educação', icon: School },
    { value: 'work', label: 'Trabalho', icon: Work },
    { value: 'monetization_on', label: 'Salário', icon: MonetizationOn },
    { value: 'show_chart', label: 'Investimento', icon: ShowChart },
    { value: 'card_giftcard', label: 'Presente', icon: CardGiftcard },
    { value: 'directions_car', label: 'Carro', icon: DirectionsCar },
    { value: 'flight', label: 'Avião', icon: Flight },
    { value: 'directions_bus', label: 'Ônibus', icon: DirectionsBus },
    { value: 'directions_bike', label: 'Bicicleta', icon: DirectionsBike },
    { value: 'coffee', label: 'Café', icon: Coffee },
    { value: 'local_grocery_store', label: 'Supermercado', icon: LocalGroceryStore },
    { value: 'local_pharmacy', label: 'Farmácia', icon: LocalPharmacy },
    { value: 'local_hospital', label: 'Hospital', icon: LocalHospital },
    { value: 'medical_services', label: 'Médico', icon: MedicalServices },
    { value: 'fitness_center', label: 'Academia', icon: FitnessCenter },
    { value: 'sports_esports', label: 'Esportes', icon: SportsEsports },
    { value: 'movie', label: 'Cinema', icon: Movie },
    { value: 'music_note', label: 'Música', icon: MusicNote },
    { value: 'book', label: 'Livro', icon: Book },
    { value: 'luggage', label: 'Viagem', icon: Luggage },
    { value: 'hotel', label: 'Hotel', icon: Hotel },
    { value: 'credit_card', label: 'Cartão', icon: CreditCard }
  ];

  const colorOptions = [
    { value: '#1976d2', label: 'Azul' },
    { value: '#dc004e', label: 'Rosa' },
    { value: '#ff6b6b', label: 'Vermelho' },
    { value: '#4ecdc4', label: 'Verde-água' },
    { value: '#45b7d1', label: 'Azul claro' },
    { value: '#96ceb4', label: 'Verde' },
    { value: '#ffeaa7', label: 'Amarelo' },
    { value: '#dda0dd', label: 'Lavanda' },
    { value: '#ffb347', label: 'Laranja' },
    { value: '#ff8c69', label: 'Salmão' },
    { value: '#87ceeb', label: 'Azul céu' },
    { value: '#c0c0c0', label: 'Prata' },
    { value: '#32cd32', label: 'Verde lima' },
    { value: '#228B22', label: 'Verde floresta' },
    { value: '#ffd700', label: 'Dourado' },
    { value: '#ff69b4', label: 'Rosa quente' },
    { value: '#90ee90', label: 'Verde claro' },
    { value: '#98fb98', label: 'Verde pálido' }
  ];

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box position="relative">
            <TextField
              fullWidth
              label="Nome da Categoria"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              error={!!errors.name}
              helperText={errors.name}
              required
            />
            <Tooltip title="Informe um nome curto e descritivo para a categoria. Máximo de 50 caracteres.">
              <IconButton 
                size="small" 
                sx={{ position: 'absolute', top: 12, right: -8 }}
              >
                <HelpOutlineIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box position="relative">
            <TextField
              fullWidth
              label="Descrição (opcional)"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              error={!!errors.description}
              helperText={errors.description}
              multiline
              rows={3}
            />
            <Tooltip title="Adicione uma descrição mais detalhada para a categoria (opcional). Máximo de 200 caracteres.">
              <IconButton 
                size="small" 
                sx={{ position: 'absolute', top: 12, right: -8 }}
              >
                <HelpOutlineIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Box position="relative">
            <FormControl fullWidth>
              <InputLabel>Tipo</InputLabel>
              <Select
                value={formData.type}
                label="Tipo"
                onChange={(e) => handleChange('type', e.target.value)}
              >
                <MenuItem value={CategoryType.EXPENSE}>Despesa</MenuItem>
                <MenuItem value={CategoryType.INCOME}>Receita</MenuItem>
              </Select>
            </FormControl>
            <Tooltip title="Selecione se esta categoria será usada para despesas (saídas de dinheiro) ou receitas (entradas de dinheiro).">
              <IconButton 
                size="small" 
                sx={{ position: 'absolute', top: 12, right: -8 }}
              >
                <HelpOutlineIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Box position="relative">
            <FormControl fullWidth>
              <InputLabel>Ícone</InputLabel>
              <Select
                value={formData.icon}
                label="Ícone"
                onChange={(e) => handleChange('icon', e.target.value)}
              >
              {iconOptions.map((icon) => {
                const IconComponent = icon.icon;
                return (
                  <MenuItem key={icon.value} value={icon.value}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Box
                        sx={{
                          width: 24,
                          height: 24,
                          borderRadius: '50%',
                          backgroundColor: formData.color,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          mr: 1
                        }}
                      >
                        {React.createElement(IconComponent, { sx: { color: 'white' } })}
                      </Box>
                      {icon.label}
                    </Box>
                  </MenuItem>
                );
              })}
            </Select>
          </FormControl>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box position="relative">
            <FormControl fullWidth error={!!errors.color}>
              <InputLabel>Cor</InputLabel>
              <Select
                value={formData.color}
                label="Cor"
                onChange={(e) => handleChange('color', e.target.value)}
              >
              {colorOptions.map((color) => (
                <MenuItem key={color.value} value={color.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box
                      sx={{
                        width: 20,
                        height: 20,
                        borderRadius: '50%',
                        backgroundColor: color.value,
                        mr: 1,
                        border: '1px solid #ccc'
                      }}
                    />
                    {color.label} ({color.value})
                  </Box>
                </MenuItem>
              ))}
            </Select>
            {errors.color && <FormHelperText>{errors.color}</FormHelperText>}
          </FormControl>
          </Box>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
        <Button onClick={onCancel} variant="outlined">
          Cancelar
        </Button>
        <Button type="submit" variant="contained">
          {category ? 'Atualizar' : 'Criar'} Categoria
        </Button>
      </Box>
    </Box>
  );
};

export default CategoryForm;