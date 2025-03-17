export interface Nodo {
  padre_id: any;
  id: number;
  nombre: string;
  titulo: string;
  tipo_cargo: 'directo' | 'asesoria';
}