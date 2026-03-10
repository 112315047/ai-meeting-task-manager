import React, { useState } from 'react';

const TaskForm = ({ onTaskCreate }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    // Pass title and description. You can adjust depending on your backend schema.
    const success = await onTaskCreate({ title, description });
    if (success) {
      setTitle('');
      setDescription('');
    }
  };

  return (
    <div className="card mb-4" style={{ padding: '1.5rem' }}>
      <h3 className="mb-2">Add New Task</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group" style={{ flexDirection: 'column', gap: '0.5rem' }}>
          <input
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            autoFocus
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button type="submit" className="btn-primary" disabled={!title.trim()}>
          Add Task
        </button>
      </form>
    </div>
  );
};

export default TaskForm;
