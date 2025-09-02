import { useNotification } from '../contexts/NotificationContext';

type NotificationType = 'success' | 'error' | 'info' | 'warning';

export const useToast = () => {
  const { addNotification } = useNotification();

  const showToast = (message: string, type: NotificationType = 'info', duration = 5000) => {
    addNotification(message, type, duration);
  };

  const success = (message: string, duration?: number) => {
    showToast(message, 'success', duration);
  };

  const error = (message: string, duration?: number) => {
    showToast(message, 'error', duration);
  };

  const info = (message: string, duration?: number) => {
    showToast(message, 'info', duration);
  };

  const warning = (message: string, duration?: number) => {
    showToast(message, 'warning', duration);
  };

  return {
    showToast,
    success,
    error,
    info,
    warning,
  };
};