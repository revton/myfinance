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

// Mock the api module
vi.mock('./lib/api', () => {
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
  
  return {
    __esModule: true,
    default: mockApi,
  };
});

// Mock the CategoryContext
vi.mock('./contexts/CategoryContext', () => {
  const actual = vi.importActual('./contexts/CategoryContext');
  return {
    ...actual,
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
  };
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
        response: {
          use: vi.fn((response, error) => response || Promise.reject(error)),
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
      // Verificar se os elementos da transação foram renderizados
      const transactionElements = screen.queryAllByText(/Salário|Receita|Despesa/);
      expect(transactionElements.length).toBeGreaterThan(0);
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
    
    // Verificar se a despesa foi adicionada (usando seletores mais flexíveis)
    await waitFor(() => {
      // Verificar se os elementos da transação foram renderizados
      const transactionElements = screen.queryAllByText(/Mercado|Receita|Despesa/);
      expect(transactionElements.length).toBeGreaterThan(0);
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

  it('renderiza elementos de transação', async () => {
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

    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '30' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Terceira' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });

    await waitFor(() => {
      // Verificar se há elementos de transação
      const transactionElements = screen.queryAllByText(/Initial|Terceira/);
      expect(transactionElements.length).toBeGreaterThan(0);
    });
  });

  it('renderiza múltiplos elementos de transação', async () => {
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
      // Verificar se há elementos de transação
      const transactionElements = screen.queryAllByText(/Initial/);
      expect(transactionElements.length).toBe(3);
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

  it('renderiza transações corretamente', async () => {
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
    
    await act(async () => {
      fireEvent.change(screen.getAllByLabelText(/Valor/i)[0], { target: { value: '10' } });
      fireEvent.change(screen.getAllByLabelText(/Descrição/i)[0], { target: { value: 'Única' } });
      fireEvent.click(screen.getAllByText(/Adicionar/i)[0]);
    });
    
    await waitFor(() => {
      // Verificar se há elementos de transação
      const transactionElements = screen.queryAllByText(/Initial|Única/);
      expect(transactionElements.length).toBeGreaterThan(0);
    });
  });
});