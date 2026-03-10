import React, { useState } from 'react';

const NotesExtractor = ({ onExtractTasks }) => {
  const [notes, setNotes] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [error, setError] = useState(null);

  const handleExtract = async (e) => {
    e.preventDefault();
    if (!notes.trim()) return;

    setIsExtracting(true);
    setError(null);

    try {
      await onExtractTasks(notes);
      setNotes(''); // Clear on success
    } catch (err) {
      setError(err.message || 'Failed to extract tasks. Please try again.');
    } finally {
      setIsExtracting(false);
    }
  };

  return (
    <div className="card w-full">
      <h2 className="mb-2">Extract Tasks from Meeting Notes</h2>
      <p style={{ color: '#6b7280', marginBottom: '1rem', fontSize: '0.9rem' }}>
        Paste your meeting notes below and our AI will automatically identify and extract tasks for you.
      </p>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleExtract}>
        <textarea
          rows={8}
          placeholder="e.g. In today's meeting, John mentioned he will update the database schema by tomorrow. We also agreed that Alice should review the new design drafts..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          disabled={isExtracting}
        />
        
        <button 
          type="submit" 
          className="btn-primary w-full"
          disabled={!notes.trim() || isExtracting}
        >
          {isExtracting ? 'Analyzing Notes...' : 'Extract & Add Tasks'}
        </button>
      </form>
    </div>
  );
};

export default NotesExtractor;
