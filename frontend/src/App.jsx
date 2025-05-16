import React, { useState } from 'react';
import { UploadForm } from './components/UploadForm';
import { JobStatus } from './components/JobStatus';
import { fetchJobStatus, submitJob } from './services/api';

function App() {
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);

  const handleJobSubmit = (jobData) => {
    submitJob(jobData)
      .then((response) => {
        setJobId(response.jobId);
        setStatus('Submitted');
      })
      .catch((error) => {
        console.error('Error submitting job:', error);
        setStatus('Error submitting job');
      });
  };

  const refreshJobStatus = () => {
    if (jobId) {
      fetchJobStatus(jobId)
        .then((response) => {
          setStatus(response.status);
        })
        .catch((error) => {
          console.error('Error fetching job status:', error);
          setStatus('Error fetching status');
        });
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>PodVision Studio 3D MVP</h1>
      <UploadForm onSubmit={handleJobSubmit} />
      {jobId && (
        <div>
          <h2>Job ID: {jobId}</h2>
          <p>Status: {status}</p>
          <button onClick={refreshJobStatus}>Refresh Status</button>
        </div>
      )}
    </div>
  );
}

export default App;
