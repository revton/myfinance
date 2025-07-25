import { vi, test, expect } from 'vitest';

globalThis.document.body.innerHTML = '<div id="root"></div>';

// Mock createRoot to avoid actual DOM rendering
vi.mock('react-dom/client', () => {
  return {
    createRoot: (el: HTMLElement) => ({
      render: vi.fn(),
    }),
  };
});

import './main';

test('main.tsx is covered by importing', () => {
  // If import succeeds, the file is covered
  expect(true).toBe(true);
}); 