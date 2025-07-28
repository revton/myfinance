import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      include: ['src/**/*'],
      exclude: ['src/**/*.test.{ts,tsx}', 'src/setupTests.ts', 'src/vite-env.d.ts']
    },
    deps: {
      optimizer: {
        web: {
          include: ['@testing-library/react', '@testing-library/jest-dom']
        }
      }
    },
    transformMode: {
      web: [/\.[jt]sx?$/],
    },
  },
}); 