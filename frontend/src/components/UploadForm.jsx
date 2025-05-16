import React, { useState } from 'react';

interface FormData {
  audioFile: File | null;
  speakerMapping: { [key: string]: string };
}

export const UploadForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState<FormData>({
    audioFile: null,
    speakerMapping: {
      'SPEAKER_00': 'male_avatar.glb',
      'SPEAKER_01': 'female_avatar.glb',
    },
  });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFormData({ ...formData, audioFile: file });
  };

  const handleSpeakerChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    speakerId: string
  ) => {
    const newMapping = { ...formData.speakerMapping };
    newMapping[speakerId] = e.target.value;
    setFormData({ ...formData, speakerMapping: newMapping });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.audioFile) {
      onSubmit(formData);
    } else {
      alert('Please select an audio file.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          Upload Audio:
          <input type="file" accept="audio/*" onChange={handleFileChange} />
        </label>
      </div>
      <div>
        <h3>Speaker Mapping</h3>
        {Object.entries(formData.speakerMapping).map(([speakerId, model]) => (
          <div key={speakerId}>
            <label>
              {speakerId}:
              <select
                value={model}
                onChange={(e) => handleSpeakerChange(e, speakerId)}
              >
                <option value="male_avatar.glb">Male Avatar</option>
                <option value="female_avatar.glb">Female Avatar</option>
              </select>
            </label>
          </div>
        ))}
      </div>
      <button type="submit">Submit Job</button>
    </form>
  );
};
