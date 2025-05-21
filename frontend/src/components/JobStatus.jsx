import React from 'react';
import { downloadVideo } from '../services/api';

export const JobStatus = ({ status, jobId }) => {
  const handleDownload = () => {
    downloadVideo(jobId);
  };

  return (
    <div>
      <h2>Job Status</h2>
      <p>Status: {status}</p>
      {status === 'completed' && (
        <button onClick={handleDownload}>Download Video</button>
      )}
    </div>
  );
};
