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

// Eliminar nodo
const eliminarNodo = async () => {
  if (!nodeIdSeleccionado.value) return;

  try {
    await store.eliminarNodo(<number>nodeIdSeleccionado.value);
    nodeIdSeleccionado.value = null;
    await store.cargarNodos();
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

// Cargar los nodos al inicio
onMounted(async () => {
  await store.cargarNodos();
  inicializarOrganigrama();
});
</script>


<template>
  <div class="w-3/4">
    <div ref="chartContainer" class="w-full" style="width: 100%; height: 600px;"></div>

    <!-- Modal o Formulario para Agregar Nodo -->
    <div v-if="nodeIdSeleccionado !== null">
      <h3>Agregar Nodo Hijo</h3>
      <form @submit.prevent="agregarNodoHijo">
        <input v-model="nombre" placeholder="Nombre del Nodo" required class="bg-white border text-black" />
        <input v-model="titulo" placeholder="Titulo del Nodo" required class="bg-white border text-black" />
        <select v-model="tipoCargo" required class="bg-white border text-black">
          <option value="directo" class="bg-white text-black">Directo</option>
          <option value="asesoria" class="bg-white text-black">Asesoria</option>
        </select>
        <button type="submit" class="bg-sky-600 text-white">Agregar Nodo</button>
      </form>
      <button @click="eliminarNodo" class="bg-red-600 text-white mt-4">Eliminar Nodo</button>
    </div>

    <!-- Modal o Formulario para Actualizar Nodo -->
    <div v-if="nodeIdSeleccionado !== null">
      <h3>Actualizar Nodo</h3>
      <form @submit.prevent="actualizarNodo">
        <input v-model="nombre" placeholder="Nombre del Nodo" required class="bg-white border text-black" />
        <input v-model="titulo" placeholder="Titulo del Nodo" required class="bg-white border text-black" />
        <select v-model="tipoCargo" required class="bg-white border text-black">
          <option value="directo" class="bg-white text-black">Directo</option>
          <option value="asesoria" class="bg-white text-black">Asesoria</option>
        </select>
        <!-- Selección del nuevo padre del nodo -->
        <select v-model="padreId" class="bg-white border text-black">
          <option value="" disabled selected>Seleccionar un nuevo padre</option>
          <option v-for="nodo in store.nodos" :key="nodo.id" :value="nodo.id">
            {{ nodo.nombre }} <!-- Solo se muestra el nombre del nodo -->
          </option>
        </select>
        <button type="submit" class="bg-sky-600 text-white">Actualizar Nodo</button>
      </form>
    </div>
  </div>
</template>



<style scoped>
h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
