import React from 'react';
import {
  Category as CategoryIcon,
  Home as HomeIcon,
  Fastfood as FoodIcon,
  Commute as TransportIcon,
  ShoppingCart as ShoppingIcon,
  TheaterComedy as EntertainmentIcon,
  LocalHospital as HealthIcon,
  School as EducationIcon,
  Work as WorkIcon,
  AttachMoney as SalaryIcon,
  TrendingUp as InvestmentIcon,
  CardGiftcard as GiftIcon,
  Restaurant as RestaurantIcon,
  DirectionsCar as CarIcon,
  Flight as PlaneIcon,
  Train as TrainIcon,
  DirectionsBus as BusIcon,
  DirectionsBike as BikeIcon,
  DirectionsWalk as WalkIcon,
  Coffee as CoffeeIcon,
  LocalBar as BeerIcon,
  WineBar as WineIcon,
  LocalPizza as PizzaIcon,
  LunchDining as BurgerIcon,
  RamenDining as SushiIcon,
  LocalGroceryStore as GroceryIcon,
  LocalPharmacy as PharmacyIcon,
  LocalHospital as HospitalIcon,
  LocalPharmacy as DoctorIcon, // Reusing LocalPharmacy for Doctor
  FitnessCenter as GymIcon,
  SportsSoccer as SportsIcon,
  Movie as MovieIcon,
  MusicNote as MusicIcon,
  Book as BookIcon,
  SportsEsports as GameIcon,
  FlightTakeoff as TravelIcon,
  Hotel as HotelIcon,
  BeachAccess as BeachIcon,
  Landscape as MountainIcon,
  CreditCard as CreditCardIcon,
  AccountBalanceWallet as WalletIcon,
  AccountBalance as BankIcon,
  Money as CashIcon
} from '@mui/icons-material';

interface IconProps {
  sx?: object;
}

export const getIconComponent = (iconName: string): React.ComponentType<IconProps> => {
  switch (iconName) {
    case 'category': return CategoryIcon;
    case 'home': return HomeIcon;
    case 'food': return FoodIcon;
    case 'transport': return TransportIcon;
    case 'shopping': return ShoppingIcon;
    case 'entertainment': return EntertainmentIcon;
    case 'health': return HealthIcon;
    case 'education': return EducationIcon;
    case 'work': return WorkIcon;
    case 'salary': return SalaryIcon;
    case 'investment': return InvestmentIcon;
    case 'gift': return GiftIcon;
    case 'restaurant': return RestaurantIcon;
    case 'car': return CarIcon;
    case 'plane': return PlaneIcon;
    case 'train': return TrainIcon;
    case 'bus': return BusIcon;
    case 'bike': return BikeIcon;
    case 'walk': return WalkIcon;
    case 'coffee': return CoffeeIcon;
    case 'beer': return BeerIcon;
    case 'wine': return WineIcon;
    case 'pizza': return PizzaIcon;
    case 'burger': return BurgerIcon;
    case 'sushi': return SushiIcon;
    case 'grocery': return GroceryIcon;
    case 'pharmacy': return PharmacyIcon;
    case 'hospital': return HospitalIcon;
    case 'doctor': return DoctorIcon;
    case 'gym': return GymIcon;
    case 'sports': return SportsIcon;
    case 'movie': return MovieIcon;
    case 'music': return MusicIcon;
    case 'book': return BookIcon;
    case 'game': return GameIcon;
    case 'travel': return TravelIcon;
    case 'hotel': return HotelIcon;
    case 'beach': return BeachIcon;
    case 'mountain': return MountainIcon;
    case 'shopping_cart': return ShoppingIcon;
    case 'credit_card': return CreditCardIcon;
    case 'wallet': return WalletIcon;
    case 'bank': return BankIcon;
    case 'cash': return CashIcon;
    default: return CategoryIcon;
  }
};
