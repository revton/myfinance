import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { act } from 'react';
import App from './App';
import axios from 'axios';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import Dashboard from './components/Dashboard';
import { MemoryRouter } from 'react-router-dom';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('MyFinance App', () => {
  beforeEach(() => {
    localStorage.setItem('access_token', 'fake-token');

    // Mock da instância do Axios e seus interceptors
    const mockApi = {
      get: vi.fn(),
      post: vi.fn(),
      interceptors: {
        request: {
          use: vi.fn((config) => config),
        },
      },
    };

    mockedAxios.create.mockReturnValue(mockApi as any);

    mockApi.get.mockResolvedValue({ data: [] });
    mockApi.post.mockImplementation(async (url: string, data: any) => ({ data }));
  });

  afterEach(() => {
    localStorage.removeItem('access_token');
  });

  it('renderiza o formulário e a lista', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    expect(screen.getByText(/Nova Transação/i)).toBeTruthy();
    expect(screen.getByText(/Transações/i)).toBeTruthy();
    expect(screen.getByText(/Nenhuma transação cadastrada/i)).toBeTruthy();
  });

  it('cadastra uma nova receita e exibe na lista', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '123.45' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Salário' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
            expect(screen.getByText(/^\+\s*R\$\s*123,45$/)).toBeTruthy();
      expect(screen.getByText(/Salário/)).toBeTruthy();
    });
  });

  it('cadastra uma nova despesa e exibe na lista', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    // Aguardar o componente carregar completamente
    await waitFor(() => {
      expect(screen.getByText(/Nova Transação/i)).toBeTruthy();
    });
    
    // Selecionar o tipo "Despesa"
    const selectElement = screen.getByLabelText(/Tipo/i);
    await act(async () => {
      fireEvent.mouseDown(selectElement);
    });
    
    // Clicar na opção Despesa
    await act(async () => {
      const despesaOption = await screen.findByText('💸 Despesa');
      fireEvent.click(despesaOption);
    });
    
    // Preencher o formulário
    await act(async () => {
      fireEvent.change(screen.getByLabelText(/Valor/i), { target: { value: '50' } });
      fireEvent.change(screen.getByLabelText(/Descrição/i), { target: { value: 'Mercado' } });
      fireEvent.click(screen.getByText(/Adicionar/i));
    });
    
    // Verificar se a despesa foi adicionada (usando regex mais flexível)
    await waitFor(() => {
      const list = screen.getByRole('list');
      const listItem = within(list).getByText(/Mercado/);
      expect(listItem).toBeTruthy();
      expect(within(list).getByText(/-\s*R\$\s*50,00/)).toBeTruthy();
    }, { timeout: 3000 });
  });

  it('exibe lista vazia se axios.get falhar', async () => {
    (mockedAxios.get as any).mockRejectedValueOnce(new Error('fail'));
    
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('usa fallback [] se axios.get retorna não-array', async () => {
    (mockedAxios.get as any).mockResolvedValueOnce({ data: { foo: 'bar' } });
    
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('renderiza Divider entre múltiplas transações', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    // Primeira transação
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Primeira' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    // Segunda transação
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '20' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Segunda' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
      // Divider: role="separator" in MUI, should be 1 for 2 items
      expect(screen.getAllByRole('separator').length).toBe(1);
    });
  });

  it('renderiza dois Dividers entre três transações', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    // Primeira transação
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Primeira' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    // Segunda transação
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '20' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Segunda' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    // Terceira transação
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '30' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Terceira' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
      expect(screen.getAllByRole('separator').length).toBe(2);
    });
  });

  it('não cadastra se descrição ou valor estiverem vazios', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    // Valor e descrição vazios
    await act(async () => {
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    
    // Valor preenchido, descrição vazia
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    
    // Valor vazio, descrição preenchida
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Teste' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
  });

  it('não renderiza Divider quando há apenas uma transação', async () => {
    await act(async () => {
      render(<MemoryRouter initialEntries={['/dashboard']}><Dashboard /></MemoryRouter>);
    });
    
    const initialSeparators = screen.queryAllByRole('separator').length;
    
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Única' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
      expect(screen.queryAllByRole('separator').length).toBe(initialSeparators);
    });
  });
});