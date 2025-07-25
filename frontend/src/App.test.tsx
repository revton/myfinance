import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';
import { describe, it, expect, beforeEach, vi } from 'vitest';

vi.mock('axios');
const mockedAxios = axios as unknown as { get: typeof axios.get; post: typeof axios.post };

describe('MyFinance App', () => {
  beforeEach(() => {
    (mockedAxios.get as any).mockResolvedValue({ data: [] });
    (mockedAxios.post as any).mockImplementation(async (_url: string, data: any) => ({ data }));
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

  it('exibe lista vazia se axios.get falhar', async () => {
    (mockedAxios.get as any).mockRejectedValueOnce(new Error('fail'));
    render(<App />);
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('usa fallback [] se axios.get retorna não-array', async () => {
    (mockedAxios.get as any).mockResolvedValueOnce({ data: { foo: 'bar' } });
    render(<App />);
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('renderiza Divider entre múltiplas transações', async () => {
    render(<App />);
    // Primeira transação
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Primeira' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    // Segunda transação
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '20' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Segunda' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    await waitFor(() => {
      // Divider: role="separator" in MUI, should be 1 for 2 items
      expect(screen.getAllByRole('separator').length).toBe(1);
    });
  });

  it('renderiza dois Dividers entre três transações', async () => {
    render(<App />);
    // Primeira transação
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Primeira' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    // Segunda transação
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '20' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Segunda' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    // Terceira transação
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '30' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Terceira' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    await waitFor(() => {
      // Divider: role="separator" in MUI, should be 2 for 3 items
      expect(screen.getAllByRole('separator').length).toBe(2);
    });
  });

  it('não cadastra se descrição ou valor estiverem vazios', async () => {
    render(<App />);
    // Valor e descrição vazios
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    // Valor preenchido, descrição vazia
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    // Valor vazio, descrição preenchida
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Teste' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
  });

  it('não renderiza Divider quando há apenas uma transação', async () => {
    render(<App />);
    const initialSeparators = screen.queryAllByRole('separator').length;
    fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
    fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Única' } });
    fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    await waitFor(() => {
      expect(screen.queryAllByRole('separator').length).toBe(initialSeparators);
    });
  });
}); 