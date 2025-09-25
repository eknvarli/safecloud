import axios from "axios";

const API_BASE = "http://localhost:8000";

export const runScan = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE}/scan/run`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};

export const getScanHistory = async () => {
  const response = await axios.get(`${API_BASE}/scan/history`);
  return response.data;
};
