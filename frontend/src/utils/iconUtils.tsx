import React from 'react';
import * as MuiIcons from '@mui/icons-material';

export const getIconComponent = (iconName: string): React.ElementType => {
  if (!iconName) {
    return MuiIcons.Category;
  }
  const pascalCaseIconName = iconName.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('');
  const IconComponent = MuiIcons[pascalCaseIconName as keyof typeof MuiIcons];
  if (IconComponent) {
    return IconComponent;
  }
  return MuiIcons.Category;
};