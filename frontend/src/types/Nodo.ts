export interface Nodo {
  padre_id: any;
  _style?: string;
  id: number;
  nombre: string;
  tipo_cargo: 'directo' | 'asesoria';
}