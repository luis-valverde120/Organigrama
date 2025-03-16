import { describe, it, expect } from 'vitest';
import { useOrganigramaStore } from '@/stores/useOrganigramaStore';

describe('useOrganigramaStore', () => {
  it('carga los nodos correctamente', async () => {
    const store = useOrganigramaStore();
    await store.cargarNodos();
    expect(store.nodos.length).toBeGreaterThan(0);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });
});