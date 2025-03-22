"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
} from "@/components/ui/menubar";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";

interface NodeActionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  selectedNode: string;
  nodes: any[];
  setNodes: (nodes: any[]) => void;
  edges: any[];
  setEdges: (edges: any[]) => void;
  apiUrl: string;  // URL de la API
}

export default function NodeActionDialog({
  isOpen,
  onClose,
  selectedNode,
  nodes,
  setNodes,
  edges,
  setEdges,
  apiUrl,
}: NodeActionDialogProps) {
  const [nodeAction, setNodeAction] = useState<"add" | "update" | "delete" | "edit" | null>(null);
  const [nodeLabel, setNodeLabel] = useState<string>("");
  const [nodeTitulo, setNodeTitulo] = useState<string>("");
  const [nodeTipoCargo, setNodeTipoCargo] = useState<string>("");
  const [nodeSuperior, setNodeSuperior] = useState<string | null>(null);
  const [nodeColor, setNodeColor] = useState<string>("#000000");
  const [textColor, setTextColor] = useState<string>("#000000");
  const [nodeBgColor, setNodeBgColor] = useState<string>("#ffffff");
  const [isBold, setIsBold] = useState<boolean>(false); // Para negritas

  // Supongamos que obtienes el valor de la base de datos, por ejemplo:
  const fetchedTitulo = "CEO"; // Este valor proviene de la base de datos.

  // Actualiza el estado con el valor recibido
  useEffect(() => {
    setNodeTitulo(fetchedTitulo); // Esto se ejecuta cuando los datos se cargan
  }, [fetchedTitulo]);

  // Para mantener los nodos existentes al actualizar
  const [availableNodes, setAvailableNodes] = useState<any[]>([]);

  // Reinicia los estados cada vez que se cierra el diálogo
  useEffect(() => {
    if (!isOpen) {
      setNodeAction(null);
      setNodeLabel("");
      setNodeTitulo("");
      setNodeTipoCargo("");
      setNodeSuperior(null);
      setNodeColor("#000000");
      setTextColor("#000000");
      setNodeBgColor("#ffffff");
      setIsBold(false);
    }
  }, [isOpen]);

  // Obtener nodos disponibles de la API
  useEffect(() => {
    if (isOpen) {
      fetch(`${apiUrl}/nodos`)
        .then((res) => res.json())
        .then((data) => setAvailableNodes(data))
        .catch((error) => console.error("Error al obtener los nodos:", error));
    }
  }, [isOpen, apiUrl]);

  // Función para seleccionar la acción "Actualizar" y precargar el label actual
  const handleSelectUpdate = () => {
    setNodeAction("update");

    // Hacer la solicitud GET usando axios
    const url = `${apiUrl}/nodos/${selectedNode}`;

    axios.get(url)
      .then((response) => {
        const data = response.data;

        // Si la respuesta contiene el nodo, rellenamos los campos
        if (data) {
          setNodeLabel(data.nombre || "");
          setNodeTitulo(data.titulo || "CEO"); // Valor predeterminado "CEO"
          setNodeTipoCargo(data.tipo_cargo || "directo"); // Valor predeterminado "directo"
          setNodeSuperior(data.padre_id || null);
        } else {
          console.error("No se encontró el nodo con ID:", selectedNode);
        }
      })
      .catch((error) => {
        console.error("Error al obtener los datos del nodo:", error);
      });
  };

  // Función para agregar un nodo hijo
  const handleAddNode = async () => {
    if (!selectedNode) {
      alert("Seleccione un nodo para agregar un hijo");
      return;
    }

    const newNode = {
      nombre: nodeLabel,
      titulo: nodeTitulo,
      tipo_cargo: nodeTipoCargo,
      color: nodeColor,
      textColor: textColor,
      bgColor: nodeBgColor,
      isBold: isBold,
      padre_id: selectedNode,
    };

    try {
      const response = await axios.post("http://localhost:3000/nodos", newNode);
      const createdNode = response.data;

      setNodes([
        ...nodes,
        {
          id: createdNode.id.toString(),
          data: { label: createdNode.nombre },
          position: { x: Math.random() * 250, y: Math.random() * 250 },
        },
      ]);
      setEdges([
        ...edges,
        { id: `e${selectedNode}-${createdNode.id}`, source: selectedNode, target: createdNode.id.toString() },
      ]);
    } catch (error) {
      console.error("Error al agregar nodo", error);
    }
  };

  // Función para actualizar un nodo (nombre, título, tipo_cargo y superior)
  // Función para actualizar un nodo (nombre, título, tipo_cargo y superior)
  const handleUpdateNode = () => {
    if (nodeLabel && nodeTitulo && nodeTipoCargo && selectedNode) {
      const nodeId = selectedNode;

      const updatedNode = {
        nombre: nodeLabel,
        titulo: nodeTitulo,
        tipo_cargo: nodeTipoCargo,
        padre_id: nodeSuperior,
      };

      const url = `${apiUrl}/nodos/${nodeId}`;

      axios
        .put(url, updatedNode)
        .then((response: { data: any; }) => {
          const data = response.data;
          setNodes(
            nodes.map((n) =>
              n.id === nodeId
                ? {
                  ...n,
                  nombre: nodeLabel,
                  titulo: nodeTitulo,
                  tipo_cargo: nodeTipoCargo,
                  padre_id: nodeSuperior,
                }
                : n
            )
          );
          onClose();
        })
        .catch((error) => console.error("Error al actualizar el nodo:", error));
    } else {
      console.error("Faltan campos para actualizar el nodo.");
    }
  };

  // Obtener nodos disponibles de la API
  useEffect(() => {
    if (isOpen) {
      axios
        .get(`${apiUrl}/nodos`)
        .then((response) => setAvailableNodes(response.data))
        .catch((error) => console.error("Error al obtener los nodos:", error));
    }
  }, [isOpen, apiUrl]);

  // Función para editar el nodo (colores, negrita)
  const handleEditNode = () => {
    if (selectedNode) {
      const updatedNode = {
        color: nodeColor,
        textColor: textColor,
        bgColor: nodeBgColor,
        isBold: isBold,
      };

      fetch(`${apiUrl}/nodos/${selectedNode}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedNode),
      })
        .then((res) => res.json())
        .then((data) => {
          setNodes(
            nodes.map((n) =>
              n.id === selectedNode
                ? { ...n, data: { ...n.data, style: { borderColor: nodeColor, backgroundColor: nodeBgColor, color: textColor, fontWeight: isBold ? "bold" : "normal" } } }
                : n
            )
          );
          onClose();
        })
        .catch((error) => console.error("Error al editar el nodo:", error));
    }
  };

  // Función para eliminar un nodo
  const handleDeleteNode = () => {
    if (selectedNode) {
      const confirmDelete = window.confirm("¿Estás seguro de que deseas eliminar este nodo?");
      if (confirmDelete) {
        fetch(`${apiUrl}/nodos/${selectedNode}`, {
          method: "DELETE",
        })
          .then(() => {
            setNodes(nodes.filter((n) => n.id !== selectedNode));
            setEdges(edges.filter((e) => e.source !== selectedNode && e.target !== selectedNode));
            onClose();
          })
          .catch((error) => console.error("Error al eliminar el nodo:", error));
      }
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            <VisuallyHidden>Acción para el Nodo</VisuallyHidden>
          </DialogTitle>
        </DialogHeader>

        <Menubar>
          <MenubarMenu>
            <MenubarTrigger asChild>
              <button className="w-full bg-blue-500 text-white py-2 rounded-lg">
                Seleccionar Acción
              </button>
            </MenubarTrigger>
            <MenubarContent>
              <MenubarItem onSelect={() => setNodeAction("add")}>Agregar Nodo</MenubarItem>
              <MenubarItem onSelect={handleSelectUpdate}>Actualizar Nodo</MenubarItem>
              <MenubarItem onSelect={() => setNodeAction("delete")}>Eliminar Nodo</MenubarItem>
              <MenubarItem onSelect={() => setNodeAction("edit")}>Edición de Nodo</MenubarItem>
            </MenubarContent>
          </MenubarMenu>
        </Menubar>

        {nodeAction === "add" && (
          <div className="mt-4 p-4 border rounded-lg bg-gray-50">
            <p className="mb-2 font-semibold">Agregar Nodo</p>
            <Input
              value={nodeLabel}
              onChange={(e) => setNodeLabel(e.target.value)}
              placeholder="Nombre del Nodo"
              className="mb-2"
            />
            <Input
              value={nodeTitulo}
              onChange={(e) => setNodeTitulo(e.target.value)}
              placeholder="Título del Nodo"
              className="mb-2"
            />
            <select
              onChange={(e) => setNodeTipoCargo(e.target.value)}
              className="mb-2 w-full px-2 my-4"
            >
              <option value="">Seleccione el tipo de cargo</option>
              <option value="directo">
                Directo
              </option>
              <option value="asesoria">
                Asesoria
              </option>
            </select>
            <select
              onChange={(e) => setNodeSuperior(e.target.value || null)}
              className="mb-2 w-full px-2 my-4"
            >
              <option value="">Seleccione Nodo Superior</option>
              {availableNodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.nombre}
                </option>
              ))}
            </select>
            <Button onClick={handleAddNode} className="w-full bg-blue-500 text-white">
              Agregar Nodo
            </Button>
          </div>
        )}

        {nodeAction === "update" && (
          <div className="mt-4 p-4 border rounded-lg bg-gray-50">
            <p className="mb-2 font-semibold">Actualizar Nodo</p>
            <Input
              value={nodeLabel}
              onChange={(e) => setNodeLabel(e.target.value)}
              placeholder="Nombre del Nodo"
              className="mb-2"
            />
            <Input
              value={nodeTitulo}
              onChange={(e) => setNodeTitulo(e.target.value)}
              placeholder="Título del Nodo"
              className="mb-2"
            />
            <select
              value={nodeTipoCargo}
              onChange={(e) => setNodeTipoCargo(e.target.value)}
              className="mb-2 w-full px-2 my-4"
            >
              <option value="">Seleccione el tipo de cargo</option>
              <option value="directo">
                Directo
              </option>
              <option value="asesoria">
                Asesoria
              </option>
            </select>
            <Button onClick={handleUpdateNode} className="w-full bg-blue-500 text-white">
              Actualizar Nodo
            </Button>
          </div>
        )}

        {nodeAction === "delete" && (
          <div className="mt-4 p-4 border rounded-lg bg-gray-50">
            <p className="mb-2 font-semibold">Eliminar Nodo</p>
            <p>¿Estás seguro de que deseas eliminar este nodo?</p>
            <Button onClick={handleDeleteNode} className="w-full bg-red-500 text-white">
              Eliminar Nodo
            </Button>
          </div>
        )}

        {nodeAction === "edit" && (
          <div className="mt-4 p-4 border rounded-lg bg-gray-50">
            <p className="mb-2 font-semibold">Editar Nodo</p>
            <Input
              type="color"
              value={textColor}
              onChange={(e) => setTextColor(e.target.value)}
              className="mb-2"
            />
            <Input
              type="color"
              value={nodeColor}
              onChange={(e) => setNodeColor(e.target.value)}
              className="mb-2"
            />
            <Input
              type="color"
              value={nodeBgColor}
              onChange={(e) => setNodeBgColor(e.target.value)}
              className="mb-2"
            />
            <label className="mb-2">
              <input
                type="checkbox"
                checked={isBold}
                onChange={(e) => setIsBold(e.target.checked)}
                className="mr-2"
              />
              Texto en negrita
            </label>
            <Button onClick={handleEditNode} className="w-full bg-blue-500 text-white">
              Confirmar Edición
            </Button>
          </div>
        )}

        <DialogFooter className="mt-4">
          <Button variant="outline" onClick={onClose}>
            Cancelar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
