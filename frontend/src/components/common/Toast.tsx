import React from 'react';
import { Snackbar, Alert, Stack } from '@mui/material';
import type { AlertColor } from '@mui/material';
import { useNotification } from '../../contexts/NotificationContext';

const Toast: React.FC = () => {
  const { notifications, removeNotification } = useNotification();

  const handleClose = (id: string) => {
    removeNotification(id);
  };

  return (
    <Stack spacing={2} sx={{ position: 'fixed', bottom: 24, right: 24, zIndex: 2000 }}>
      {notifications.map((notification) => (
        <Snackbar
          key={notification.id}
          open={true}
          autoHideDuration={notification.duration}
          onClose={() => handleClose(notification.id)}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          sx={{ position: 'relative', mb: 2 }}
        >
          <Alert
            onClose={() => handleClose(notification.id)}
            severity={notification.type as AlertColor}
            variant="filled"
            sx={{ width: '100%' }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      ))}
    </Stack>
  );
};

export default Toast;