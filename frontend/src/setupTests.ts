import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock @mui/icons-material to prevent EMFILE errors
vi.mock('@mui/icons-material', () => {
  return {
    __esModule: true,
    // Default export for cases like `import Icon from '@mui/icons-material';`
    default: vi.fn((props) => <div {...props}>MockIcon</div>),
    // Named exports for specific icons like `import { Add } from '@mui/icons-material';`
    // We can return a generic mock component for all named exports
    __all__: new Proxy({}, {
      get: (target, name) => {
        if (name === '__esModule') return true;
        return vi.fn((props) => <div {...props}>{String(name)}Mock</div>);
      },
    }),
  };
});

// Mock window.matchMedia for tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver 
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
