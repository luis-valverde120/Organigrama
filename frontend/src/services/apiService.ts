import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

export const fetchNodos = async () => {
  const response = await axios.get(`${API_BASE_URL}/nodos`);
  console.log(response.data)
  return response.data;
};

export const fetchNodo = async (id: number) => {
  const response = await axios.get(`${API_BASE_URL}/nodo/${id}`);
  return response.data;
};

export const addNodo = async (nodo: any) => {
  const response = await axios.post(`${API_BASE_URL}/nodos`, nodo);
  return response.data;
};

export const deleteNodo = async (id: number) => {
  const response = await axios.delete(`${API_BASE_URL}/nodos/${id}`);
  return response.status === 204;
}

// Actualizar un nodo
export const updateNodo = async (id: number, updatedData: any) => {
  const response = await axios.put(`${API_BASE_URL}/nodos/${id}`, updatedData);
  return response.data;
};
