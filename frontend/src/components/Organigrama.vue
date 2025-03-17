<script setup lang="ts">
import { ref, onMounted } from 'vue';
import OrgChart from '@balkangraph/orgchart.js';
import { useOrganigramaStore } from '../stores/useOrganigramaStore';
import type { Nodo } from '@/types';

const store = useOrganigramaStore();
const chartContainer = ref<HTMLDivElement | null>(null);
const nodeIdSeleccionado = ref<number | null>(null); // Guarda el ID del nodo seleccionado

// Variables para el formulario
const nombre = ref('');
const tipoCargo = ref<'directo' | 'asesoria'>('directo'); // Valor por defecto

// Formatear los datos para la librería
const formatearNodos = () => {
  return store.nodos.map(nodo => ({
    id: nodo.id,
    pid: nodo.padre_id || null, // `null` si no tiene jefe
    name: nodo.nombre, // Usar 'name' para que funcione con la librería
    title: nodo.tipo_cargo// Usar 'title' en lugar de 'tipo_cargo'
  }));
};

// Inicializar el organigrama
const inicializarOrganigrama = () => {
  if (chartContainer.value) {
    const chart = new OrgChart(chartContainer.value, {
      nodes: formatearNodos(),
      nodeBinding: {
        field_0: 'name',   // Mostrar el nombre del nodo
        field_1: 'title' // Mostrar el tipo de cargo del nodo
      },
    });

    chart.on('click', (sender, args) => {
      if (args.node) {
        nodeIdSeleccionado.value = args.node.id; // Capturamos el ID del nodo seleccionado
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
      nombre: nombre.value,        // ✅ Correcto
      tipo_cargo: tipoCargo.value, // 🔄 Cambiado a `tipo_cargo`
      padre_id: nodeIdSeleccionado.value // 🔄 Cambiado a `padre_id`
    });

    // Resetear formulario
    nombre.value = '';
    tipoCargo.value = 'directo';
    nodeIdSeleccionado.value = null;

    // Recargar organigrama
    await store.cargarNodos();
    inicializarOrganigrama();
  } catch (error) {
    console.error('Error al agregar nodo:', error);
  }
};

// Cargar los nodos al inicio
onMounted(async () => {
  await store.cargarNodos();
  inicializarOrganigrama();
});
</script>

<template>
  <div>
    <h2>Organigrama</h2>
    <div ref="chartContainer" style="width: 100%; height: 600px;"></div>

    <!-- Modal o Formulario para Agregar Nodo -->
    <div v-if="nodeIdSeleccionado !== null">
      <h3>Agregar Nodo Hijo</h3>
      <form @submit.prevent="agregarNodoHijo">
        <input v-model="nombre" placeholder="Nombre del Nodo" required class="bg-white border text-black" />
        <select v-model="tipoCargo" required class="bg-white border text-black">
          <option value="directo" class="bg-white text-black">Directo</option>
          <option value="asesoria" class="bg-white text-black">Asesoria</option>
        </select>
        <button type="submit" class="bg-sky-600 text-white">Agregar Nodo</button>
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
