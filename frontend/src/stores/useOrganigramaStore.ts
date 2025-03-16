import { defineStore } from 'pinia';
import { ref } from 'vue';
import { fetchNodos, addNodo, deleteNodo } from '../services/apiService';

interface Nodo {
  id: number;
  nombre: string;
  tipo: 'directo' | 'asesoria';
  id_superior?: number;
}

export const useOrganigramaStore = defineStore('organigrama', () => {
  const nodos = ref<Nodo[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Cargar todos los nodos
  const cargarNodos = async () => {
    loading.value = true;
    error.value = null;
    try {
      const data = await fetchNodos();
      nodos.value = data;
    } catch (err) {
      error.value = 'Error al cargar los nodos';
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  // Agregar un nuevo nodo
  const agregarNodo = async (nodo: Omit<Nodo, 'id'>) => {
    try {
      const nuevoNodo = await addNodo(nodo);
      nodos.value.push(nuevoNodo);
    } catch (err) {
      console.error('Error al agregar el nodo:', err);
      throw err;
    }
  };

  // Eliminar un nodo
  const eliminarNodo = async (id: number) => {
    try {
      const success = await deleteNodo(id);
      if (success) {
        nodos.value = nodos.value.filter((n) => n.id !== id);
      }
    } catch (err) {
      console.error('Error al eliminar el nodo:', err);
      throw err;
    }
  };

  return {
    nodos,
    loading,
    error,
    cargarNodos,
    agregarNodo,
    eliminarNodo,
  };
});