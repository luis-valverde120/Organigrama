import React, { useState } from "react";
import ReactFlow from "reactflow";
import NodeActionDialog from "@/components/NodeActionDialog"; // Importa el componente NodeActionDialog
import Organigrama from "@/components/organigrama";
import { useCallback } from "react";

// Componente superior que engloba ambos componentes
const OrganigramaApp = () => {
  const [nodes, setNodes] = useState([]);  // Estado para los nodos
  const [edges, setEdges] = useState([]);  // Estado para los bordes

  // Función para actualizar el nodo
  const updateNode = (updatedNodeData: { id: any; data: any; }) => {
    setNodes((prevNodes) =>
      prevNodes.map((node) =>
        node.id === updatedNodeData.id
          ? { ...node, data: { ...node.data, ...updatedNodeData.data } }
          : node
      )
    );
  };

  return (
    <div>
      <NodeActionDialog updateNode={updateNode} />
      <Organigrama nodes={nodes} edges={edges} />
    </div>
  );
};
