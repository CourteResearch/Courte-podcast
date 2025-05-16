import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const submitJob = (data) => {
  return axios.post(`${API_URL}/submit-job`, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

export const fetchJobStatus = (jobId) => {
  return axios.get(`${API_URL}/job-status/${jobId}`);
};
