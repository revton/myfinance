// src/components/common/LoadingCard.tsx
import React from 'react';
import { Card, CardContent, Skeleton } from '@mui/material';

export const LoadingCard: React.FC = () => (
  <Card>
    <CardContent>
      <Skeleton variant="text" width="60%" height={32} />
      <Skeleton variant="text" width="40%" height={24} />
      <Skeleton variant="rectangular" width="100%" height={100} />
    </CardContent>
  </Card>
);
