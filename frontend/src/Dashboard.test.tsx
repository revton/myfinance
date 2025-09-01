import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import { vi } from 'vitest';
import axios from 'axios';

// Mock MUI icons to prevent EMFILE errors
vi.mock('@mui/icons-material', () => ({
  Add: () => <div data-testid="add">Add</div>,
  Menu: () => <div data-testid="menu">Menu</div>,
  Close: () => <div data-testid="close">Close</div>,
  Home: () => <div data-testid="home">Home</div>,
  AccountBalance: () => <div data-testid="account-balance">AccountBalance</div>,
  TrendingUp: () => <div data-testid="trending-up">TrendingUp</div>,
  TrendingDown: () => <div data-testid="trending-down">TrendingDown</div>,
  Category: () => <div data-testid="category">Category</div>,
  Settings: () => <div data-testid="settings">Settings</div>,
  Logout: () => <div data-testid="logout">Logout</div>,
  Person: () => <div data-testid="person">Person</div>,
  Dashboard: () => <div data-testid="dashboard">Dashboard</div>,
  FilterList: () => <div data-testid="filter-list">FilterList</div>,
  Clear: () => <div data-testid="clear">Clear</div>,
  CalendarToday: () => <div data-testid="calendar-today">CalendarToday</div>,
  AttachMoney: () => <div data-testid="attach-money">AttachMoney</div>,
  CheckCircle: () => <div data-testid="check-circle">CheckCircle</div>,
  RadioButtonUnchecked: () => <div data-testid="radio-button-unchecked">RadioButtonUnchecked</div>,
  Note: () => <div data-testid="note">Note</div>,
  Label: () => <div data-testid="label">Label</div>,
  CreditCard: () => <div data-testid="credit-card">CreditCard</div>,
  LocalGroceryStore: () => <div data-testid="local-grocery-store">LocalGroceryStore</div>,
  Restaurant: () => <div data-testid="restaurant">Restaurant</div>,
  LocalHospital: () => <div data-testid="local-hospital">LocalHospital</div>,
  DirectionsCar: () => <div data-testid="directions-car">DirectionsCar</div>,
  School: () => <div data-testid="school">School</div>,
  Work: () => <div data-testid="work">Work</div>,
  Flight: () => <div data-testid="flight">Flight</div>,
  LocalActivity: () => <div data-testid="local-activity">LocalActivity</div>,
  SportsEsports: () => <div data-testid="sports-esports">SportsEsports</div>,
  Movie: () => <div data-testid="movie">Movie</div>,
  MusicNote: () => <div data-testid="music-note">MusicNote</div>,
  Book: () => <div data-testid="book">Book</div>,
  FitnessCenter: () => <div data-testid="fitness-center">FitnessCenter</div>,
  LocalPharmacy: () => <div data-testid="local-pharmacy">LocalPharmacy</div>,
  Hotel: () => <div data-testid="hotel">Hotel</div>,
  Luggage: () => <div data-testid="luggage">Luggage</div>,
  Coffee: () => <div data-testid="coffee">Coffee</div>,
  DirectionsBus: () => <div data-testid="directions-bus">DirectionsBus</div>,
  DirectionsBike: () => <div data-testid="directions-bike">DirectionsBike</div>,
  HealthAndSafety: () => <div data-testid="health-and-safety">HealthAndSafety</div>,
  MedicalServices: () => <div data-testid="medical-services">MedicalServices</div>,
  CardGiftcard: () => <div data-testid="card-giftcard">CardGiftcard</div>,
  ShowChart: () => <div data-testid="show-chart">ShowChart</div>,
  MonetizationOn: () => <div data-testid="monetization-on">MonetizationOn</div>,
  ShoppingCart: () => <div data-testid="shopping-cart">ShoppingCart</div>,
  Commute: () => <div data-testid="commute">Commute</div>,
}));

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock the CategoryContext
vi.mock('./contexts/CategoryContext', () => ({
  useCategories: () => ({
    categories: [],
    expenseCategories: [],
    incomeCategories: [],
    loading: false,
    error: null,
    createCategory: vi.fn(),
    updateCategory: vi.fn(),
    deleteCategory: vi.fn(),
    restoreCategory: vi.fn(),
    getCategoriesByType: vi.fn(() => []),
    getCategoryById: vi.fn(),
  }),
}));

describe('Dashboard', () => {
  beforeEach(() => {
    // Create a proper mock for axios instance
    const mockApi = {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: {
          use: vi.fn(),
        },
        response: {
          use: vi.fn(),
        },
      },
    };
    
    // Mock axios.create to return our mockApi
    mockedAxios.create.mockReturnValue(mockApi as any);
    mockApi.get.mockResolvedValue({ data: [] });
  });

  it('renders without crashing', async () => {
    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(screen.getByText(/Nova Transação/i)).toBeInTheDocument();
  });

  it('displays empty state when no transactions', async () => {
    const mockApi = mockedAxios.create();
    mockApi.get.mockResolvedValueOnce({ data: [] });
    
    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    expect(screen.getByText(/Nenhuma transação cadastrada/i)).toBeInTheDocument();
  });

  it('displays transactions when available', async () => {
    const mockTransactions = [
      {
        id: '1',
        type: 'income',
        amount: 1000,
        description: 'Monthly Salary',
        created_at: '2023-01-01T00:00:00Z',
        category_id: '1',
        category: {
          id: '1',
          name: 'Salary',
          icon: 'monetization_on',
          type: 'income',
          color: '#4caf50'
        }
      }
    ];

    const mockApi = mockedAxios.create();
    mockApi.get.mockResolvedValueOnce({ data: mockTransactions });
    
    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    );

    // Wait for transactions to load - using a more specific selector
    expect(await screen.findByText(/Monthly Salary/i)).toBeInTheDocument();
  });
});