import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock @mui/icons-material to prevent EMFILE errors
vi.mock('@mui/icons-material', () => {
  const React = require('react');
  const mockIcon = (props: any) => React.createElement('div', props, 'MockIcon');
  
  return {
    __esModule: true,
    // Mock all icons as the same component to prevent import issues
    Category: mockIcon,
    Home: mockIcon,
    Restaurant: mockIcon,
    Commute: mockIcon,
    ShoppingCart: mockIcon,
    LocalActivity: mockIcon,
    HealthAndSafety: mockIcon,
    School: mockIcon,
    Work: mockIcon,
    MonetizationOn: mockIcon,
    ShowChart: mockIcon,
    CardGiftcard: mockIcon,
    DirectionsCar: mockIcon,
    Flight: mockIcon,
    DirectionsBus: mockIcon,
    DirectionsBike: mockIcon,
    Coffee: mockIcon,
    LocalGroceryStore: mockIcon,
    LocalPharmacy: mockIcon,
    LocalHospital: mockIcon,
    MedicalServices: mockIcon,
    FitnessCenter: mockIcon,
    SportsEsports: mockIcon,
    Movie: mockIcon,
    MusicNote: mockIcon,
    Book: mockIcon,
    Luggage: mockIcon,
    Hotel: mockIcon,
    CreditCard: mockIcon,
    // Default export
    default: mockIcon
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
