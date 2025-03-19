"use client";
import { useCallback, useState } from "react";
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
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
} from "@/components/ui/menubar";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";

const initialNodes = [
  { id: "1", data: { label: "CEO" }, position: { x: 250, y: 0 } },
  { id: "2", data: { label: "Manager" }, position: { x: 150, y: 100 } },
  { id: "3", data: { label: "Employee" }, position: { x: 350, y: 100 } },
];

const initialEdges = [
  { id: "e1-2", source: "1", target: "2", type: "smoothstep" },
  { id: "e1-3", source: "1", target: "3", type: "smoothstep" },
];

export default function Organigrama() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [nodeAction, setNodeAction] = useState<"add" | "update" | "delete" | null>(null);
  const [nodeLabel, setNodeLabel] = useState<string>("");
  
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
    [setEdges]
  );
  
  const openModal = (nodeId: string | null) => {
    setSelectedNode(nodeId);
    setNodeAction(null); // No hay acción seleccionada inicialmente
    setNodeLabel(""); // Limpiar el campo
    setIsModalOpen(true);
  };
  
  const closeModal = () => {
    setIsModalOpen(false);
  };
  
  // Funciones de acción
  const handleAddNode = () => {
    if (nodeLabel && selectedNode) {
      const newNode = {
        id: `${nodes.length + 1}`,
        data: { label: nodeLabel },
        position: { x: 100, y: 100 },
      };
      const newEdge = {
        id: `${selectedNode}-${newNode.id}`,
        source: selectedNode,
        target: newNode.id,
        label: "to the",
      };
      setNodes([...nodes, newNode]);
      setEdges([...edges, newEdge]);
      closeModal();
    }
  };
  
  const handleUpdateNode = () => {
    if (nodeLabel && selectedNode) {
      setNodes((nds) =>
        nds.map((n) =>
          n.id === selectedNode ? { ...n, data: { label: nodeLabel } } : n
        )
      );
      closeModal();
    }
  };
  
  const handleDeleteNode = () => {
    if (selectedNode) {
      const confirmDelete = window.confirm("¿Estás seguro de que deseas eliminar este nodo?");
      if (confirmDelete) {
        setNodes((nds) => nds.filter((n) => n.id !== selectedNode));
        setEdges((eds) => eds.filter((e) => e.source !== selectedNode && e.target !== selectedNode));
        closeModal();
      }
    }
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
      <Card className="w-full h-96 bg-white rounded-lg shadow-lg p-4" id="organigrama">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onConnect={onConnect}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={(event, node) => openModal(node.id)}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </Card>
      <Button onClick={exportToPDF} className="mt-4">
        Exportar a PDF
      </Button>
  
      {/* Diálogo para seleccionar acción */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              <VisuallyHidden>Seleccionar Acción para el Nodo</VisuallyHidden>
            </DialogTitle>
          </DialogHeader>
  
          {/* Menú en forma de Menubar */}
          <Menubar>
            <MenubarMenu>
              <MenubarTrigger asChild>
                <button className="w-full bg-blue-500 text-white py-2 rounded-lg">
                  Seleccionar Acción
                </button>
              </MenubarTrigger>
              <MenubarContent>
                <MenubarItem onSelect={() => setNodeAction("add")}>
                  Agregar Nodo
                </MenubarItem>
                <MenubarItem onSelect={() => setNodeAction("update")}>
                  Actualizar Nodo
                </MenubarItem>
                <MenubarItem onSelect={() => setNodeAction("delete")}>
                  Eliminar Nodo
                </MenubarItem>
              </MenubarContent>
            </MenubarMenu>
          </Menubar>
  
          {/* Sección que muestra la acción seleccionada y sus campos */}
          {nodeAction === null && (
            <div className="mt-4 text-center">
              <p className="text-gray-600">Seleccione una acción del menú anterior.</p>
            </div>
          )}
  
          {nodeAction === "add" && (
            <div className="mt-4 p-4 border rounded-lg bg-gray-50">
              <p className="mb-2 font-semibold">Agregar Nodo Hijo</p>
              <Input
                type="text"
                value={nodeLabel}
                onChange={(e) => setNodeLabel(e.target.value)}
                placeholder="Ingrese nombre para el nuevo nodo"
                className="mb-2"
              />
              <Button onClick={handleAddNode} className="w-full bg-blue-500 text-white">
                Confirmar Agregar
              </Button>
            </div>
          )}
  
          {nodeAction === "update" && (
            <div className="mt-4 p-4 border rounded-lg bg-gray-50">
              <p className="mb-2 font-semibold">Actualizar Nodo</p>
              <Input
                type="text"
                value={nodeLabel}
                onChange={(e) => setNodeLabel(e.target.value)}
                placeholder="Ingrese nuevo nombre para el nodo"
                className="mb-2"
              />
              <Button onClick={handleUpdateNode} className="w-full bg-blue-500 text-white">
                Confirmar Actualización
              </Button>
            </div>
          )}
  
          {nodeAction === "delete" && (
            <div className="mt-4 p-4 border rounded-lg bg-red-50">
              <p className="mb-2 font-semibold text-red-600">Eliminar Nodo</p>
              <p className="mb-4">Se eliminará el nodo seleccionado. Esta acción no se puede deshacer.</p>
              <Button onClick={handleDeleteNode} className="w-full bg-red-500 text-white">
                Confirmar Eliminación
              </Button>
            </div>
          )}
  
          <DialogFooter>
            <Button variant="outline" onClick={closeModal}>
              Cancelar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
