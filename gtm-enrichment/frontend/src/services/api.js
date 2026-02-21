import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/upload`, formData);
    return response.data;
};

export const getBatchStatus = async (batchId) => {
    const response = await axios.get(`${API_BASE_URL}/batch/${batchId}`);
    return response.data;
};