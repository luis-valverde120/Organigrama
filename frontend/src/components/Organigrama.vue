<script setup lang="ts">
import { ref, onMounted } from 'vue';
import OrgChart from '@balkangraph/orgchart.js';
import { useOrganigramaStore } from '../stores/useOrganigramaStore';
import type { Nodo } from '@/types';

const store = useOrganigramaStore();
const chartContainer = ref<HTMLDivElement | null>(null);
const nodeIdSeleccionado = ref<number | null>(null); // Guarda el ID del nodo seleccionado

// Variables para el formulario de agregar y actualizar nodo
const nombre = ref('');
const tipoCargo = ref<'directo' | 'asesoria'>('directo'); // Valor por defecto
const titulo = ref('');
const padreId = ref<number | null>(null); // Variable para el padre del nodo al actualizar

// Verificar si hay nodos en el organigrama
const tieneNodos = ref(false);

// Formatear los datos para la librería
const formatearNodos = () => {
  return store.nodos.map(nodo => ({
    id: nodo.id,
    pid: nodo.padre_id || null, // `null` si no tiene jefe
    name: nodo.nombre, // Usar 'name' para que funcione con la librería
    title: nodo.titulo // Usar 'title' en lugar de 'tipo_cargo'
  }));
};

// Inicializar el organigrama
const inicializarOrganigrama = () => {
  if (chartContainer.value) {
    const chart = new OrgChart(chartContainer.value, {
      nodes: formatearNodos(),
      nodeBinding: {
        field_0: 'name',   // Mostrar el nombre del nodo
        field_1: 'title'   // Mostrar el tipo de cargo del nodo
      },
    });

    chart.on('click', (sender, args) => {
      if (args.node) {
        nodeIdSeleccionado.value = args.node.id; // Capturamos el ID del nodo seleccionado
        const nodoSeleccionado = store.nodos.find(n => n.id === nodeIdSeleccionado.value);
        if (nodoSeleccionado) {
          nombre.value = nodoSeleccionado.nombre;
          tipoCargo.value = nodoSeleccionado.tipo_cargo;
          titulo.value = nodoSeleccionado.titulo;
          padreId.value = nodoSeleccionado.padre_id || null; // Guardar el padre actual
        }
        console.log('Nodo seleccionado:', args.node); // Imprime el nodo completo
      }
    });
  }
};

// Agregar nodo hijo
const agregarNodoHijo = async () => {
  if (!nodeIdSeleccionado.value) return;

  try {
    await store.agregarNodo({
      nombre: nombre.value,
      tipo_cargo: tipoCargo.value,
      padre_id: nodeIdSeleccionado.value,
      titulo: titulo.value
    });

    // Resetear formulario
    nombre.value = '';
    tipoCargo.value = 'directo';
    nodeIdSeleccionado.value = null;
    titulo.value = '';

    // Recargar organigrama
    await store.cargarNodos();
    inicializarOrganigrama();
  } catch (error) {
    console.error('Error al agregar nodo:', error);
  }
};

// eliminar nodo
const eliminarNodo = async () => {
  if (!nodeIdSeleccionado.value) return;

  try {
    await store.eliminarNodo(<number>nodeIdSeleccionado.value);
    nodeIdSeleccionado.value = null;
    await store.cargarNodos();

    // Actualizar el estado de si tiene nodos
    tieneNodos.value = store.nodos.length > 0;  // Verifica si aún hay nodos

    // Recargar el organigrama
    inicializarOrganigrama();
  } catch (error) {
    console.error('Error al eliminar nodo:', error);
  }
};

// Actualizar nodo
const actualizarNodo = async () => {
  if (!nodeIdSeleccionado.value) return;

  try {
    await store.actualizarNodo(nodeIdSeleccionado.value, {
      nombre: nombre.value,
      tipo_cargo: tipoCargo.value,
      titulo: titulo.value,
      padre_id: padreId.value // Incluye el nuevo padre_id
    });

    // Resetear formulario de actualización
    nombre.value = '';
    tipoCargo.value = 'directo';
    titulo.value = '';
    padreId.value = null;

    // Recargar organigrama
    await store.cargarNodos();
    inicializarOrganigrama();
    nodeIdSeleccionado.value = null;
  } catch (error) {
    console.error('Error al actualizar nodo:', error);
  }
};

// Modificar después de agregar un nodo inicial
const agregarNodoInicial = async () => {
  try {
    await store.agregarNodo({
      nombre: nombre.value,
      tipo_cargo: tipoCargo.value,
      padre_id: null, // No tiene padre
      titulo: titulo.value
    });

    // Recargar organigrama y actualizar el estado de los nodos
    await store.cargarNodos();
    tieneNodos.value = store.nodos.length > 0;  // Actualiza el estado de los nodos
    inicializarOrganigrama();
  } catch (error) {
    console.error('Error al agregar nodo inicial:', error);
  }
};

// Cargar los nodos al inicio
onMounted(async () => {
  await store.cargarNodos();
  tieneNodos.value = store.nodos.length > 0;
  inicializarOrganigrama();
});
</script>

<template>
  <div class="flex">
    <div ref="chartContainer" class="w-3/4" style="height: 600px;"></div>

    <!-- Contenedor para formularios y botones -->
    <div class="w-1/4 ml-4 space-y-4">
      <!-- Mostrar formulario para agregar el primer nodo -->
      <div v-if="!tieneNodos" class="p-4 border border-gray-300 rounded-lg shadow-lg">
        <h3 class="text-xl font-semibold mb-4">Agregar Nodo Inicial</h3>

        <form @submit.prevent="agregarNodoInicial" class="space-y-4">
          <input v-model="nombre" placeholder="Nombre del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />
          <input v-model="titulo" placeholder="Titulo del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />
          <select v-model="tipoCargo" required class="w-full p-2 border border-gray-300 rounded-md">
            <option value="directo">Directo</option>
            <option value="asesoria">Asesoria</option>
          </select>

          <button type="submit" class="w-full bg-sky-600 text-white py-2 rounded-md">Agregar Nodo Inicial</button>
        </form>
      </div>

      <div v-if="nodeIdSeleccionado !== null" class="p-4 border border-gray-300 rounded-lg shadow-lg">
        <h3 class="text-xl font-semibold mb-4">Actualizar Nodo</h3>

        <!-- Formulario para actualizar nodo -->
        <form @submit.prevent="actualizarNodo" class="space-y-4">
          <input v-model="nombre" placeholder="Nombre del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />
          <input v-model="titulo" placeholder="Titulo del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />

          <select v-model="tipoCargo" required class="w-full p-2 border border-gray-300 rounded-md">
            <option value="directo">Directo</option>
            <option value="asesoria">Asesoria</option>
          </select>

          <!-- Selección del nuevo padre del nodo -->
          <select v-model="padreId" class="w-full p-2 border border-gray-300 rounded-md">
            <option value="" disabled selected>Seleccionar un nuevo padre</option>
            <option v-for="nodo in store.nodos" :key="nodo.id" :value="nodo.id">{{ nodo.nombre }}</option>
          </select>

          <button type="submit" class="w-full bg-sky-600 text-white py-2 rounded-md">Actualizar Nodo</button>
        </form>

        <!-- Botón de eliminar -->
        <button @click="eliminarNodo" class="w-full bg-red-600 text-white py-2 rounded-md mt-4">Eliminar Nodo</button>
      </div>

      <div v-if="nodeIdSeleccionado !== null" class="p-4 border border-gray-300 rounded-lg shadow-lg">
        <h3 class="text-xl font-semibold mb-4">Agregar Nodo Hijo</h3>

        <!-- Formulario para agregar nodo hijo -->
        <form @submit.prevent="agregarNodoHijo" class="space-y-4">
          <input v-model="nombre" placeholder="Nombre del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />
          <input v-model="titulo" placeholder="Titulo del Nodo" required
            class="w-full p-2 border border-gray-300 rounded-md" />

          <select v-model="tipoCargo" required class="w-full p-2 border border-gray-300 rounded-md">
            <option value="directo">Directo</option>
            <option value="asesoria">Asesoria</option>
          </select>

          <button type="submit" class="w-full bg-sky-600 text-white py-2 rounded-md">Agregar Nodo</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilo general para los formularios y botones */
input,
select {
  transition: border-color 0.3s ease;
}

input:focus,
select:focus {
  border-color: #4CAF50;
}

button:hover {
  opacity: 0.9;
}
</style>
