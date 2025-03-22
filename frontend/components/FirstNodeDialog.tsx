"use client";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface FirstNodeDialogProps {
  isOpen: boolean;
  onClose: () => void;
  setNodes: (nodes: any[]) => void;
}

export default function FirstNodeDialog({
  isOpen,
  onClose,
  setNodes,
}: FirstNodeDialogProps) {
  const [nodeLabel, setNodeLabel] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreateFirstNode = async () => {
    if (!nodeLabel) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/nodes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          label: nodeLabel,
          position: { x: 250, y: 100 },
        }),
      });

      if (!response.ok) {
        throw new Error("Error al crear el nodo");
      }

      const newNode = await response.json();
      setNodes([newNode]); // Actualizar los nodos con el nuevo nodo desde la API
      onClose();
    } catch (err: any) {
      setError(err.message || "Error desconocido");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Crear Primer Nodo</DialogTitle>
        </DialogHeader>
        <div className="mt-4">
          <Input
            type="text"
            value={nodeLabel}
            onChange={(e) => setNodeLabel(e.target.value)}
            placeholder="Ingrese nombre para el nodo"
            disabled={loading}
          />
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>
        <DialogFooter className="mt-4">
          <Button onClick={handleCreateFirstNode} className="bg-blue-500 text-white" disabled={loading}>
            {loading ? "Creando..." : "Confirmar Creación"}
          </Button>
          <Button variant="outline" onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
