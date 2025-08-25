// src/theme/index.ts
import { createTheme } from '@mui/material/styles';
import { dashboardColors } from './colors';
import { dashboardTypography } from './typography';

export const theme = createTheme({
  palette: {
    primary: {
      main: dashboardColors.primary,
    },
    secondary: {
      main: dashboardColors.secondary,
    },
    success: {
      main: dashboardColors.success,
    },
    error: {
      main: dashboardColors.error,
    },
    warning: {
      main: dashboardColors.warning,
    },
    info: {
      main: dashboardColors.info,
    },
    background: {
      default: dashboardColors.background,
      paper: dashboardColors.surface,
    },
    text: {
      primary: dashboardColors.text.primary,
      secondary: dashboardColors.text.secondary,
      disabled: dashboardColors.text.disabled,
    },
  },
  typography: dashboardTypography,
});
