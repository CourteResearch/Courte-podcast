import React, { useState } from 'react';

export const UploadForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    audioFile: null,
    speakerMapping: {
      SPEAKER_00: 'male_avatar.glb',
      SPEAKER_01: 'female_avatar.glb',
    },
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files?.[0] || null;
    setFormData((prev) => ({ ...prev, audioFile: file }));
    setSuccess(false);
    setError('');
  };

  const handleSpeakerChange = (e, speakerId) => {
    const newMapping = {
      ...formData.speakerMapping,
      [speakerId]: e.target.value,
    };
    setFormData((prev) => ({ ...prev, speakerMapping: newMapping }));
    setSuccess(false);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess(false);
    setError('');
    if (formData.audioFile) {
      setLoading(true);
      const data = new FormData();
      data.append('audio_file', formData.audioFile);
      data.append('speaker_mapping', JSON.stringify(formData.speakerMapping));
      try {
        await onSubmit(data);
        setSuccess(true);
      } catch (err) {
        setError('Failed to submit. Please try again.');
      }
      setLoading(false);
    } else {
      setError('Please select an audio file.');
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: 400,
        margin: '2rem auto',
        padding: '2rem',
        borderRadius: 12,
        boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
        background: '#fff',
        fontFamily: 'Segoe UI, Arial, sans-serif',
      }}
    >
      <h2 style={{ textAlign: 'center', marginBottom: 24, color: '#2d3748' }}>
        🎙️ PodVision Studio Job Submission
      </h2>
      <div style={{ marginBottom: 18 }}>
        <label style={{ fontWeight: 500, color: '#4a5568' }}>
          Upload Audio:
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            style={{
              display: 'block',
              marginTop: 8,
              padding: 8,
              borderRadius: 6,
              border: '1px solid #cbd5e1',
              width: '100%',
            }}
            disabled={loading}
          />
        </label>
      </div>
      <div style={{ marginBottom: 18 }}>
        <h3 style={{ color: '#2b6cb0', marginBottom: 8 }}>Speaker Mapping</h3>
        {Object.entries(formData.speakerMapping).map(([speakerId, model]) => (
          <div key={speakerId} style={{ marginBottom: 10 }}>
            <label style={{ color: '#4a5568', fontWeight: 500 }}>
              {speakerId}:
              <select
                value={model}
                onChange={(e) => handleSpeakerChange(e, speakerId)}
                style={{
                  marginLeft: 8,
                  padding: 6,
                  borderRadius: 6,
                  border: '1px solid #cbd5e1',
                }}
                disabled={loading}
              >
                <option value="male_avatar.glb">Male Avatar</option>
                <option value="female_avatar.glb">Female Avatar</option>
              </select>
            </label>
          </div>
        ))}
      </div>
      <button
        type="submit"
        disabled={loading}
        style={{
          width: '100%',
          padding: '12px 0',
          background: loading ? '#a0aec0' : '#3182ce',
          color: '#fff',
          fontWeight: 600,
          border: 'none',
          borderRadius: 8,
          fontSize: 16,
          cursor: loading ? 'not-allowed' : 'pointer',
          transition: 'background 0.2s',
        }}
      >
        {loading ? 'Submitting...' : 'Submit Job'}
      </button>
      {success && (
        <div
          style={{
            marginTop: 18,
            padding: 12,
            background: '#e6fffa',
            color: '#2c7a7b',
            borderRadius: 6,
            textAlign: 'center',
            fontWeight: 500,
          }}
        >
          ✅ Job submitted successfully!
        </div>
      )}
      {error && (
        <div
          style={{
            marginTop: 18,
            padding: 12,
            background: '#fed7d7',
            color: '#c53030',
            borderRadius: 6,
            textAlign: 'center',
            fontWeight: 500,
          }}
        >
          {error}
        </div>
      )}
    </form>
  );
};
