import React from 'react';
import { Box, CircularProgress, Typography, Button, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';

const LoadingContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '200px',
  width: '100%',
  position: 'relative',
  overflow: 'hidden',
}));

const PulseAnimation = styled(Box)(({ theme }) => ({
  '@keyframes pulse': {
    '0%': {
      opacity: 0.6,
      transform: 'scale(0.98)',
    },
    '50%': {
      opacity: 0.8,
      transform: 'scale(1)',
    },
    '100%': {
      opacity: 0.6,
      transform: 'scale(0.98)',
    },
  },
  animation: 'pulse 1.5s infinite',
  width: '100%',
}));

interface AdvancedLoadingStateProps {
  isLoading: boolean;
  error?: Error | null;
  onRetry?: () => void;
  loadingText?: string;
  errorText?: string;
  children: React.ReactNode;
  height?: string | number;
  showSkeleton?: boolean;
}

const AdvancedLoadingState: React.FC<AdvancedLoadingStateProps> = ({
  isLoading,
  error,
  onRetry,
  loadingText = 'Carregando dados...',
  errorText = 'Ocorreu um erro ao carregar os dados.',
  children,
  height = '100%',
  showSkeleton = true,
}) => {
  return (
    <Box sx={{ height, width: '100%', position: 'relative' }}>
      {/* Loading State */}
      {isLoading && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: 10,
            animation: 'fadeIn 300ms ease-out forwards',
            '@keyframes fadeIn': {
              '0%': {
                opacity: 0,
              },
              '100%': {
                opacity: 1,
              }
            }
          }}
        >
          <LoadingContainer elevation={0}>
            <CircularProgress size={40} thickness={4} />
            <Typography variant="body1" sx={{ mt: 2 }}>
              {loadingText}
            </Typography>
            {showSkeleton && (
              <Box sx={{ width: '100%', mt: 3 }}>
                <PulseAnimation sx={{ height: '20px', borderRadius: '4px', bgcolor: 'rgba(0,0,0,0.1)', mb: 1 }} />
                <PulseAnimation sx={{ height: '100px', borderRadius: '4px', bgcolor: 'rgba(0,0,0,0.1)', mb: 1 }} />
                <PulseAnimation sx={{ height: '20px', borderRadius: '4px', bgcolor: 'rgba(0,0,0,0.1)', width: '60%' }} />
              </Box>
            )}
          </LoadingContainer>
        </Box>
      )}

      {/* Error State */}
      {!!error && !isLoading && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: 10,
            animation: 'fadeIn 300ms ease-out forwards',
            '@keyframes fadeIn': {
              '0%': {
                opacity: 0,
              },
              '100%': {
                opacity: 1,
              }
            }
          }}
        >
          <LoadingContainer elevation={0}>
            <Typography variant="h6" color="error" gutterBottom>
              {errorText}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {error?.message}
            </Typography>
            {onRetry && (
              <Button
                variant="contained"
                color="primary"
                onClick={onRetry}
                sx={{ mt: 2 }}
              >
                Tentar novamente
              </Button>
            )}
          </LoadingContainer>
        </Box>
      )}

      {/* Content */}
      <Box
        sx={{
          opacity: isLoading || !!error ? 0.3 : 1,
          transition: 'opacity 0.3s ease',
          height: '100%',
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default AdvancedLoadingState;