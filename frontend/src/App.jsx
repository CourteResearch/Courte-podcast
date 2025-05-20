import React, { useState, useEffect, useRef } from 'react';
import { UploadForm } from './components/UploadForm';
import { fetchJobStatus, submitJob } from './services/api';

function App() {
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [outputPath, setOutputPath] = useState('');
  const [progress, setProgress] = useState(0);
  const [polling, setPolling] = useState(false);
  const intervalRef = useRef(null);

  const handleJobSubmit = async (jobData) => {
    setStatus(null);
    setOutputPath('');
    setJobId(null);
    try {
      const response = await submitJob(jobData);
      if (response && response.data && response.data.job_id) {
        setJobId(response.data.job_id);
        setStatus('Processing...');
        setPolling(true);
      } else {
        setStatus('Error: Invalid response from backend');
        console.error('Invalid backend response:', response);
      }
    } catch (error) {
      setStatus('Error submitting job');
      if (error.response) {
        console.error('Backend error:', error.response.data);
      } else {
        console.error('Network or unknown error:', error);
      }
    }
  };

  useEffect(() => {
    if (polling && jobId) {
      intervalRef.current = setInterval(() => {
        fetchJobStatus(jobId)
          .then((response) => {
            const data = response.data || response;
            setStatus(data.status);
            setOutputPath(data.output_path);
            setProgress(data.progress || 0);
            if (data.status === 'completed' || data.status === 'failed') {
              setPolling(false);
              clearInterval(intervalRef.current);
            }
          })
          .catch((error) => {
            console.error('Error fetching job status:', error);
            setStatus('Error fetching status');
            setPolling(false);
            clearInterval(intervalRef.current);
          });
      }, 2000);
      return () => clearInterval(intervalRef.current);
    }
  }, [polling, jobId]);

  const handleDownload = () => {
    if (jobId && status === 'completed') {
      window.open(`http://localhost:8000/download/${jobId}`, '_blank');
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #e0e7ff 0%, #f0fff4 100%)',
        padding: '40px 0',
      }}
    >
      <h1
        style={{
          textAlign: 'center',
          color: '#2b6cb0',
          fontWeight: 800,
          fontSize: 36,
          marginBottom: 32,
          letterSpacing: 1,
        }}
      >
        PodVision Studio 3D MVP
      </h1>
      <UploadForm onSubmit={handleJobSubmit} />
      {jobId && (
        <div
          style={{
            maxWidth: 400,
            margin: '2rem auto',
            padding: '1.5rem',
            borderRadius: 12,
            background: '#fff',
            boxShadow: '0 2px 12px rgba(0,0,0,0.07)',
            textAlign: 'center',
          }}
        >
          <h2 style={{ color: '#2d3748', fontWeight: 700, marginBottom: 12 }}>
            Job ID: {jobId}
          </h2>
          <p
            style={{
              color:
                status === 'completed'
                  ? '#2c7a7b'
                  : status === 'failed'
                  ? '#c53030'
                  : '#4a5568',
              fontWeight: 500,
              fontSize: 18,
              marginBottom: 18,
            }}
          >
            Status: {status}
          </p>
          {status === 'completed' && (
            <button
              onClick={handleDownload}
              style={{
                padding: '12px 24px',
                background: '#38a169',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                fontWeight: 600,
                fontSize: 16,
                cursor: 'pointer',
                marginTop: 10,
              }}
            >
              Download Video
            </button>
          )}
          {status === 'failed' && (
            <div
              style={{
                marginTop: 10,
                color: '#c53030',
                fontWeight: 600,
              }}
            >
              Video processing failed. Please try again.
            </div>
          )}
          {status !== 'completed' && status !== 'failed' && (
            <div style={{ marginTop: 10 }}>
              <div
                style={{
                  width: '100%',
                  height: 18,
                  background: '#e2e8f0',
                  borderRadius: 8,
                  overflow: 'hidden',
                  marginBottom: 8,
                }}
              >
                <div
                  style={{
                    width: `${progress}%`,
                    height: '100%',
                    background: '#3182ce',
                    transition: 'width 0.5s',
                  }}
                />
              </div>
              <span
                style={{
                  color: '#4a5568',
                  fontWeight: 500,
                  fontSize: 14,
                }}
              >
                {progress}% - Please wait while your video is being processed...
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
