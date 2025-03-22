'use client';
import { useCallback, useEffect, useState } from "react";
import ReactFlow, {
  Controls,
  Background,
  addEdge,
  Connection,
  Edge,
  applyEdgeChanges,
  applyNodeChanges,
} from "reactflow";
import "reactflow/dist/style.css";
import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import EmptyState from "@/components/EmptyState";
import NodeActionDialog from "@/components/NodeActionDialog";
import FirstNodeDialog from "@/components/FirstNodeDialog";
import axios from "axios";

const initialNodes: any[] = [];
const initialEdges: Edge[] = [];

type NodoAPI = {
  id: number;
  nombre: string;
  titulo: string;
  padre_id?: number | null;
  tipo_cargo?: string;
  color_fondo?: string;
  color_borde?: string;
  color_texto?: string;
};

const API_URL = 'http://127.0.0.1:5000';

export default function Organigrama() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const response = await axios.get<NodoAPI[]>(`${API_URL}/nodos`); // Reemplaza con tu URL real
      const datos = response.data;

      const { nuevosNodos, nuevosEdges } = transformarDatosAReactFlow(datos);
      setNodes(nuevosNodos);
      setEdges(nuevosEdges);
    } catch (error) {
      console.error("Error al obtener los datos:", error);
    }
  };

  const transformarDatosAReactFlow = (datos: NodoAPI[]) => {
    const nuevosNodos = datos.map((nodo) => ({
      id: nodo.id.toString(),
      data: { label: `${nodo.nombre} (${nodo.titulo})` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      type: "default",
      style: {
        backgroundColor: nodo.color_fondo || "#ffffff",
        borderColor: nodo.color_borde || "#000000",
        borderWidth: 2,
        padding: "10px",
        textAlign: "center",
        color: nodo.color_texto || "#000000",
      },
    }));

    const nuevosEdges = datos
      .filter((nodo) => nodo.padre_id !== null && nodo.padre_id !== undefined)
      .map((nodo) => ({
        id: `edge-${nodo.id}`,
        source: nodo.padre_id!.toString(),
        target: nodo.id.toString(),
        animated: false,
        type: "step", // Tipo step para líneas
        style: nodo.tipo_cargo === "asesoria"
          ? { strokeDasharray: "5,5", stroke: "gray" } // Línea entrecortada para asesores
          : { stroke: "black" },
      }));

    return { nuevosNodos, nuevosEdges };
  };

  // Cargar los datos en el estado cuando el componente se monta
  useEffect(() => {
    fetchData();
  }, []);

  const onNodesChange = useCallback(
    (changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );
  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  const openFirstNodeDialog = () => {
    setSelectedNode(null);
    setIsDialogOpen(true);
  };

  const openNodeActionDialog = (nodeId: string) => {
    setSelectedNode(nodeId);
    setIsDialogOpen(true);
  };

  const closeDialog = () => {
    setIsDialogOpen(false);
  };

  const exportToPDF = async () => {
    const input = document.getElementById("organigrama");
    if (!input) {
      console.error("Element with id 'organigrama' not found.");
      return;
    }
    const canvas = await html2canvas(input);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF();
    pdf.addImage(imgData, "PNG", 10, 10, 190, 0);
    pdf.save("organigrama.pdf");
  };

  return (
    <div className="h-screen flex flex-col items-center bg-gray-100 p-5 w-2/3">
      <h1 className="text-3xl font-bold mb-4 text-gray-800">Organigrama</h1>
      {nodes.length === 0 ? (
        <EmptyState onCreate={openFirstNodeDialog} />
      ) : (
        <Card className="w-full h-96 bg-white rounded-lg shadow-lg p-4" id="organigrama">
          <ReactFlow
            key={JSON.stringify(nodes)}  // Esto actualizará el key cada vez que los nodos cambien
            nodes={nodes}
            edges={edges}
            onConnect={onConnect}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={(event, node) => openNodeActionDialog(node.id)}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </Card>
      )}
      <Button onClick={exportToPDF} className="mt-4">
        Exportar a PDF
      </Button>

      {nodes.length > 0 && selectedNode && (
        <NodeActionDialog
          apiUrl={API_URL}
          isOpen={isDialogOpen}
          onClose={closeDialog}
          selectedNode={selectedNode}
          nodes={nodes}
          setNodes={setNodes}
          edges={edges}
          setEdges={setEdges}
        />
      )}

      {nodes.length === 0 && (
        <FirstNodeDialog
          isOpen={isDialogOpen}
          onClose={closeDialog}
          setNodes={setNodes}
        />
      )}
    </div>
  );
}
