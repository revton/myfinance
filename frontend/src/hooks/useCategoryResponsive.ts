import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

export const useCategoryResponsive = () => {
  const theme = useTheme();
  
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  
  const getGridSize = () => {
    if (isMobile) return 12;
    if (isTablet) return 6;
    return 4;
  };
  
  const getCardHeight = () => {
    if (isMobile) return 'auto';
    return '200px';
  };
  
  return { 
    isMobile, 
    isTablet, 
    isDesktop, 
    getGridSize, 
    getCardHeight 
  };
};
