import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { describe, it, expect, beforeEach, vi } from 'vitest';

vi.mock('axios');
const mockedAxios = axios as unknown as { get: typeof axios.get; post: typeof axios.post };

describe('MyFinance App', () => {
  beforeEach(() => {
    (mockedAxios.get as jest.Mock).mockResolvedValue({ data: [] });
    (mockedAxios.post as jest.Mock).mockImplementation(async (_url: string, data: unknown) => ({ data }));
  });

  it('renderiza o formulário e a lista', async () => {
    render(<App />);
    expect(screen.getByText(/Nova Transação/i)).toBeTruthy();
    expect(screen.getByText(/Transações/i)).toBeTruthy();
    expect(screen.getByText(/Nenhuma transação cadastrada/i)).toBeTruthy();
  });

  it('cadastra uma nova receita e exibe na lista', async () => {
    render(<App />);
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '123.45' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Salário' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    await waitFor(() => {
      expect(screen.getByText(/Receita: R\$ 123.45/)).toBeTruthy();
      expect(screen.getByText(/Salário/)).toBeTruthy();
    });
  });

  it('cadastra uma nova despesa e exibe na lista', async () => {
    render(<App />);
    // Simular seleção do tipo usando mouseDown e click no MenuItem
    fireEvent.mouseDown(screen.getAllByLabelText(/Tipo/i)[0].parentElement!.querySelector('[role=combobox]')!);
    fireEvent.click(await screen.findByText('Despesa'));
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '50' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Mercado' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    await waitFor(() => {
      expect(screen.getByText(/Despesa: R\$ 50.00/)).toBeTruthy();
      expect(screen.getByText(/Mercado/)).toBeTruthy();
    });
  });
}); 