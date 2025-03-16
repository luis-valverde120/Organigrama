<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import OrgChart from '@balkangraph/orgchart.js';
import { useOrganigramaStore } from '../stores/useOrganigramaStore';

const store = useOrganigramaStore();
const chartContainer = ref<HTMLDivElement | null>(null);
let chart: OrgChart | null = null;

// Formatear los datos para la librería
const formatearNodos = () => {
  return store.nodos.map(nodo => ({
    id: nodo.id,
    pid: nodo.id_superior || null, // `null` si no tiene jefe
    name: nodo.nombre,
    tags: [nodo.tipo] // Opcional: Agregar estilos según tipo
  }));
};

// Inicializar organigrama
const inicializarOrganigrama = () => {
  if (chartContainer.value) {
    chart = new OrgChart(chartContainer.value, {
      nodes: formatearNodos(),
      nodeBinding: {
        field_0: 'name'
      }
    });
  }
};

// Cargar datos al montar
onMounted(async () => {
  await store.cargarNodos();
  inicializarOrganigrama();
});

// Re-renderizar cuando cambien los nodos
watch(() => store.nodos, () => {
  if (chart) {
    chart.load(formatearNodos());
  }
}, { deep: true });
</script>

<template>
  <div>
    <h2>Organigrama</h2>
    <div ref="chartContainer" style="width: 100%; height: 600px;"></div>
  </div>
</template>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
