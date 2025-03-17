import { defineStore } from 'pinia';
import { ref } from 'vue';
import { fetchNodos, addNodo, deleteNodo, updateNodo } from '../services/apiService';
import type { Nodo } from '@/types';

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

  // Actualizar un nodo
  const actualizarNodo = async (id: number, updatedData: Omit<Nodo, 'id'>) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedNodo = await updateNodo(id, updatedData); // Llamada al servicio para actualizar el nodo
      const index = nodos.value.findIndex((nodo) => nodo.id === id);
      if (index !== -1) {
        nodos.value[index] = updatedNodo; // Actualiza el nodo en el array de nodos
      }
    } catch (err) {
      error.value = 'Error al actualizar el nodo';
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  return {
    nodos,
    loading,
    error,
    cargarNodos,
    agregarNodo,
    eliminarNodo,
    actualizarNodo,
  };
});