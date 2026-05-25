import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const queryRAGSystem = async (userId: string, query: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/query`, {
      user_id: userId,
      query: query,
    });
    return response.data;
  } catch (error) {
    console.error('Error querying RAG system:', error);
    throw error;
  }
};

export const getDocuments = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/documents`);
    return response.data;
  } catch (error) {
    console.error('Error fetching documents:', error);
    throw error;
  }
};

export const getAuditLogs = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/audit-logs`);
    return response.data;
  } catch (error) {
    console.error('Error fetching audit logs:', error);
    throw error;
  }
};

export const getUsers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users`);
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

export const getMetrics = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/metrics`);
    return response.data;
  } catch (error) {
    console.error('Error fetching metrics:', error);
    throw error;
  }
};
