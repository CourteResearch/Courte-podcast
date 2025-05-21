import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const submitJob = (formData) => {
  return axios.post(`${API_URL}/submit-job`, formData);
};

export const fetchJobStatus = (jobId) => {
  return axios.get(`${API_URL}/job-status/${jobId}`);
};

export const downloadVideo = (jobId) => {
  // We don't use axios here because we want to trigger a direct file download
  // and axios is typically for JSON responses.
  window.open(`${API_URL}/download/${jobId}`, '_blank');
};
