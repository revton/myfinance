import { render, screen, fireEvent, waitFor, act, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import axios from 'axios';
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { ThemeProvider, createTheme } from '@mui/material/styles';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

vi.mock('@mui/material/styles', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useTheme: () => ({
      breakpoints: {
        down: vi.fn((breakpoint) => `(max-width:${breakpoint})`),
      },
    }),
    createTheme: (actual as any).createTheme,
  };
});

vi.mock('@mui/material/useMediaQuery', () => ({
  __esModule: true,
  default: vi.fn(() => false),
}));

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  })),
});

describe('Dashboard Component', () => {

  let theme: ReturnType<typeof createTheme>;

  let mockApi: {
    get: vi.fn,
    post: vi.fn,
    interceptors: {
      request: {
        use: vi.fn,
      },
    },
  };

  beforeEach(() => {
    localStorage.setItem('access_token', 'fake-token');
    theme = createTheme();

    mockApi = {
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
    mockApi.post.mockImplementation(async (url: string, data: any) => ({ 
        data: {
            id: 'mock-id-' + Math.random(),
            created_at: new Date().toISOString(),
            ...data,
        }
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
    // Explicitly reset window.matchMedia mock
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })),
    });
  });

  it('renderiza o formulário e a lista', async () => {
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    expect(screen.getByText(/Nova Transação/i)).toBeTruthy();
    expect(screen.getByText(/Transações/i)).toBeTruthy();
    expect(screen.getByText(/Nenhuma transação cadastrada/i)).toBeTruthy();
  });

  it('cadastra uma nova receita e exibe na lista', async () => {
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '123.45' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Salário' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
      const list = screen.getByRole('list');
      const listItem = within(list).getByText(/Salário/);
      expect(listItem).toBeTruthy();
      expect(within(list).getByText(/\+\s*R\$\s*123,45/)).toBeTruthy();
    });
  });

  it('cadastra uma nova despesa e exibe na lista', async () => {
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    // Aguardar o componente carregar completamente
    await waitFor(() => {
      expect(screen.getByText(/Nova Transação/i)).toBeTruthy();
    });
    
    // Selecionar o tipo "Despesa"
    const selectElement = screen.getByLabelText(/Tipo/i);
    await act(async () => {
      fireEvent.mouseDown(selectElement);
      fireEvent.click(selectElement); // Click to open the dropdown
    });
    
    // Clicar na opção Despesa
    await act(async () => {
      const despesaOption = await screen.findByRole('option', { name: /Despesa/i });
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
    mockApi.get.mockRejectedValueOnce(new Error('fail'));
    
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('usa fallback [] se axios.get retorna não-array', async () => {
    mockApi.get.mockResolvedValueOnce({ data: { foo: 'bar' } });
    
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    await waitFor(() => {
      expect(screen.getAllByText(/Nenhuma transa[cç]ão cadastrada/i).length).toBeGreaterThan(0);
    });
  });

  it('renderiza Divider entre múltiplas transações', async () => {
    // Mock initial transactions for this test
    mockApi.get.mockResolvedValueOnce({
      data: [
        { id: '1', type: 'income', amount: 10, description: 'Initial 1', created_at: new Date().toISOString() },
        { id: '2', type: 'expense', amount: 5, description: 'Initial 2', created_at: new Date().toISOString() },
      ],
    });

    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );

    await waitFor(() => {
      expect(screen.getByText(/Initial 1/)).toBeInTheDocument();
    });
    
    // Add a third transaction to trigger the second divider
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '30' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Terceira' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });

    await waitFor(() => {
      // Divider: role="separator" in MUI, should be 2 for 3 items
      expect(screen.getAllByRole('separator').length).toBe(2);
    });
  });

  it('renderiza dois Dividers entre três transações', async () => {
    // Mock initial transactions for this test
    mockApi.get.mockResolvedValueOnce({
      data: [
        { id: '1', type: 'income', amount: 10, description: 'Initial 1', created_at: new Date().toISOString() },
        { id: '2', type: 'expense', amount: 5, description: 'Initial 2', created_at: new Date().toISOString() },
        { id: '3', type: 'income', amount: 20, description: 'Initial 3', created_at: new Date().toISOString() },
      ],
    });

    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
    await waitFor(() => {
      // Divider: role="separator" in MUI, should be 2 for 3 items
      expect(screen.getAllByRole('separator').length).toBe(2);
    });
  });

  it('não cadastra se descrição ou valor estiverem vazios', async () => {
    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
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
    // Mock initial transactions for this test
    mockApi.get.mockResolvedValueOnce({
      data: [
        { id: '1', type: 'income', amount: 10, description: 'Initial 1', created_at: new Date().toISOString() },
      ],
    });

    render(
      <ThemeProvider theme={theme}>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Dashboard />
        </MemoryRouter>
      </ThemeProvider>
    );
    
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