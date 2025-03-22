"use client";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  onCreate: () => void;
}

export default function EmptyState({ onCreate }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center w-full h-96 bg-white rounded-lg shadow-lg p-4">
      <p className="text-lg text-gray-600 mb-4">Aún no hay nodos en el organigrama.</p>
      <Button onClick={onCreate} className="bg-blue-500 text-white">
        Agregar Primer Nodo
      </Button>
    </div>
  );
}
