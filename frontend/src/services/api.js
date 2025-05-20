import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const submitJob = (formData) => {
  return axios.post(`${API_URL}/submit-job`, formData);
};

export const fetchJobStatus = (jobId) => {
  return axios.get(`${API_URL}/job-status/${jobId}`);
};
