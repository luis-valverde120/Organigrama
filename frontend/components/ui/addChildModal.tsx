// AddChildModal.tsx
import * as Dialog from '@radix-ui/react-dialog';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface AddChildModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddChild: (newNodeLabel: string, selectedNodeId: string) => void;
  selectedNode: string | null;
}

const AddChildModal: React.FC<AddChildModalProps> = ({ isOpen, onClose, onAddChild, selectedNode }) => {
  const [nodeLabel, setNodeLabel] = useState("");

  const handleAddChild = () => {
    if (nodeLabel && selectedNode) {
      onAddChild(nodeLabel, selectedNode);
      onClose(); // Cierra el modal después de agregar el hijo
    }
  };

  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Overlay className="fixed inset-0 bg-black opacity-50" />
      <Dialog.Content className="fixed top-1/4 left-1/2 transform -translate-x-1/2 p-6 bg-white rounded-lg shadow-lg">
        <Dialog.Title className="text-xl mb-4">Agregar Hijo</Dialog.Title>
        <input
          type="text"
          placeholder="Nombre del nodo"
          value={nodeLabel}
          onChange={(e) => setNodeLabel(e.target.value)}
          className="border p-2 mb-4 w-full"
        />
        <div className="flex justify-between">
          <Button onClick={handleAddChild}>Agregar</Button>
          <Button onClick={onClose}>Cerrar</Button>
        </div>
      </Dialog.Content>
    </Dialog.Root>
  );
};

export default AddChildModal;
