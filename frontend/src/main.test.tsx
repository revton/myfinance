import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { vi } from 'vitest';

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

describe('Main App', () => {
  it('renders without crashing', () => {
    render(<App />);

    // Simple test to check if the app renders
    expect(true).toBe(true);
  });
});