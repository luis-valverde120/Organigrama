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
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
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

const initialNodes: any[] = []; // Inicialmente vacío o con nodos
const initialEdges: Edge[] = [];

export default function Organigrama() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [nodeAction, setNodeAction] = useState<"add" | "update" | "delete" | null>(null);
  const [nodeLabel, setNodeLabel] = useState<string>("");
  // Estado para estilos: color de borde, color de letras y fondo del nodo
  const [nodeColor, setNodeColor] = useState<string>("#000000");
  const [textColor, setTextColor] = useState<string>("#000000");
  const [nodeBgColor, setNodeBgColor] = useState<string>("#ffffff");
  const [showDeleteButton, setShowDeleteButton] = useState(false);

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

  // Abre el modal para acciones sobre nodos existentes
  const openModal = (nodeId: string | null) => {
    setSelectedNode(nodeId);
    setNodeAction(null);
    setNodeLabel("");
    setNodeColor("#000000");
    setTextColor("#000000");
    setNodeBgColor("#ffffff");
    setShowDeleteButton(false);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  // Función para agregar un nuevo nodo hijo a un nodo existente
  const handleAddNode = () => {
    if (nodeLabel && selectedNode) {
      const parentNode = nodes.find((node) => node.id === selectedNode);
      const newNode = {
        id: `${nodes.length + 1}`,
        data: { label: nodeLabel, parentId: selectedNode },
        position: {
          x: parentNode?.position.x + 150,
          y: parentNode?.position.y + 100,
        },
      };
      const newEdge = {
        id: `${selectedNode}-${newNode.id}`,
        source: selectedNode,
        target: newNode.id,
        type: "smoothstep",
      };
      setNodes([...nodes, newNode]);
      setEdges([...edges, newEdge]);
      closeModal();
    }
  };

  // Función para actualizar un nodo (nombre y estilos)
  const handleUpdateNode = () => {
    if (nodeLabel && selectedNode) {
      setNodes((nds) =>
        nds.map((n) =>
          n.id === selectedNode
            ? {
                ...n,
                data: { ...n.data, label: nodeLabel },
                style: {
                  ...n.style,
                  border: `2px solid ${nodeColor}`,
                  color: textColor,
                  backgroundColor: nodeBgColor,
                },
              }
            : n
        )
      );
      closeModal();
    }
  };

  // Función para eliminar un nodo existente
  const handleDeleteNode = () => {
    if (selectedNode) {
      const confirmDelete = window.confirm("¿Estás seguro de que deseas eliminar este nodo?");
      if (confirmDelete) {
        setNodes((nds) => nds.filter((n) => n.id !== selectedNode));
        setEdges((eds) =>
          eds.filter((e) => e.source !== selectedNode && e.target !== selectedNode)
        );
        closeModal();
      }
    }
  };

  // Para crear el primer nodo cuando no hay ninguno (sin conexiones)
  const openCreateFirstNodeModal = () => {
    setSelectedNode(null);
    setNodeAction("add");
    setNodeLabel("");
    setNodeColor("#000000");
    setTextColor("#000000");
    setNodeBgColor("#ffffff");
    setIsModalOpen(true);
  };

  const handleCreateFirstNode = () => {
    if (nodeLabel) {
      const newNode = {
        id: "1",
        data: { label: nodeLabel },
        position: { x: 250, y: 100 },
      };
      setNodes([newNode]);
      closeModal();
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

      {nodes.length === 0 ? (
        // Estado vacío: mensaje y CTA para crear el primer nodo
        <div className="flex flex-col items-center justify-center w-full h-96 bg-white rounded-lg shadow-lg p-4">
          <p className="text-lg text-gray-600 mb-4">Aún no hay nodos en el organigrama.</p>
          <Button onClick={openCreateFirstNodeModal} className="bg-blue-500 text-white">
            Agregar Primer Nodo
          </Button>
        </div>
      ) : (
        // Organigrama interactivo
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
      )}

      <Button onClick={exportToPDF} className="mt-4">
        Exportar a PDF
      </Button>

      {/* Diálogo para acciones */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              <VisuallyHidden>Acción para el Nodo</VisuallyHidden>
            </DialogTitle>
          </DialogHeader>

          {/* Si es el primer nodo */}
          {nodes.length === 0 || (nodes.length > 0 && selectedNode === null) ? (
            <div className="mt-4 p-4 border rounded-lg bg-gray-50">
              <p className="mb-2 font-semibold">Crear Primer Nodo</p>
              <Input
                type="text"
                value={nodeLabel}
                onChange={(e) => setNodeLabel(e.target.value)}
                placeholder="Ingrese nombre para el nodo"
                className="mb-2"
              />
              <Button onClick={handleCreateFirstNode} className="w-full bg-blue-500 text-white">
                Confirmar Creación
              </Button>
            </div>
          ) : (
            <>
              {/* Menubar para seleccionar la acción */}
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
                    <MenubarItem
                      onSelect={() => {
                        setNodeAction("update");
                        const current = nodes.find((n) => n.id === selectedNode);
                        if (current) {
                          setNodeLabel(current.data.label);
                        }
                      }}
                    >
                      Actualizar Nodo
                    </MenubarItem>
                    <MenubarItem onSelect={() => setNodeAction("delete")}>
                      Eliminar Nodo
                    </MenubarItem>
                  </MenubarContent>
                </MenubarMenu>
              </Menubar>

              {/* Indicador de acción seleccionada */}
              {nodeAction && (
                <p className="mt-2 text-center text-gray-700 font-medium">
                  Acción seleccionada:{" "}
                  {nodeAction === "add"
                    ? "Agregar"
                    : nodeAction === "update"
                    ? "Actualizar"
                    : "Eliminar"}
                </p>
              )}

              {/* Sección condicional según la acción */}
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
                  <div className="mb-2">
                    <label htmlFor="nodeColor" className="block text-sm font-medium text-gray-700">
                      Color del Borde
                    </label>
                    <Input
                      id="nodeColor"
                      type="color"
                      value={nodeColor}
                      onChange={(e) => setNodeColor(e.target.value)}
                      className="w-full"
                    />
                  </div>
                  <div className="mb-2">
                    <label htmlFor="nodeTextColor" className="block text-sm font-medium text-gray-700">
                      Color de las Letras
                    </label>
                    <Input
                      id="nodeTextColor"
                      type="color"
                      value={textColor}
                      onChange={(e) => setTextColor(e.target.value)}
                      className="w-full"
                    />
                  </div>
                  <div className="mb-2">
                    <label htmlFor="nodeBgColor" className="block text-sm font-medium text-gray-700">
                      Color del Nodo
                    </label>
                    <Input
                      id="nodeBgColor"
                      type="color"
                      value={nodeBgColor}
                      onChange={(e) => setNodeBgColor(e.target.value)}
                      className="w-full"
                    />
                  </div>
                  <Button onClick={handleUpdateNode} className="w-full bg-blue-500 text-white">
                    Confirmar Actualización
                  </Button>
                </div>
              )}

              {nodeAction === "delete" && (
                <div className="mt-4 p-4 border rounded-lg bg-red-50">
                  <p className="mb-2 font-semibold text-red-600">Eliminar Nodo</p>
                  <p className="mb-4">
                    Se eliminará el nodo seleccionado. Esta acción no se puede deshacer.
                  </p>
                  <Button onClick={handleDeleteNode} className="w-full bg-red-500 text-white">
                    Confirmar Eliminación
                  </Button>
                </div>
              )}
            </>
          )}

          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={closeModal}>
              Cancelar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
