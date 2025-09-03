import React from 'react';
import { Box } from '@mui/material';

interface AnimatedListProps {
  children: React.ReactNode;
  className?: string;
}

const AnimatedList: React.FC<AnimatedListProps> = ({
  children,
  className,
}) => {
  return (
    <Box className={className}>
      {React.Children.map(children, (child, index) => (
        React.isValidElement(child) ? React.cloneElement(child, {
          ...child.props,
          key: child.key || index,
          sx: {
            ...((child.props as any)?.sx || {}),
            animation: `fadeIn ${300 + index * 100}ms ease-out forwards`,
            '@keyframes fadeIn': {
              '0%': {
                opacity: 0,
                transform: 'translateY(10px)'
              },
              '100%': {
                opacity: 1,
                transform: 'translateY(0)'
              }
            }
          }
        }) : child
      ))}
    </Box>
  );
};

export default AnimatedList;