import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  IconButton,
  Chip,
  Tooltip
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Lock as LockIcon
} from '@mui/icons-material';
import type { Category } from '../../types/category';
import { getIconComponent } from '../../utils/iconUtils';

interface CategoryCardProps {
  category: Category;
  onEdit: () => void;
  onDelete: () => void;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category, onEdit, onDelete }) => {
  const IconComponent = getIconComponent(category.icon); 
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: '50%',
              backgroundColor: category.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2
            }}
          >
            <IconComponent sx={{ color: 'white', fontSize: 30 }} /> 
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" gutterBottom>
              {category.name}
            </Typography>
            <Chip 
              label={category.type === 'expense' ? 'Despesa' : 'Receita'} 
              size="small" 
              color={category.type === 'expense' ? 'error' : 'success'}
            />
            {category.is_default && (
              <Chip 
                label="Padrão" 
                size="small" 
                variant="outlined"
                sx={{ ml: 1 }}
              />
            )}
          </Box>
        </Box>
        
        {category.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {category.description}
          </Typography>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Criada em {new Date(category.created_at).toLocaleDateString('pt-BR')}
          </Typography>
          {category.is_default && (
            <Tooltip title="Categoria padrão - não pode ser excluída">
              <LockIcon color="action" fontSize="small" />
            </Tooltip>
          )}
        </Box>
      </CardContent>

      {!category.is_default && (
        <CardActions sx={{ justifyContent: 'flex-end' }}>
          <IconButton onClick={onEdit} color="primary" size="small">
            <EditIcon />
          </IconButton>
          <IconButton onClick={onDelete} color="error" size="small">
            <DeleteIcon />
          </IconButton>
        </CardActions>
      )}
    </Card>
  );
};

export default CategoryCard;
