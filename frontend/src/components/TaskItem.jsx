import React from 'react';

const TaskItem = ({ task, onToggle, onDelete }) => {
  const isCompleted = task.status === 'completed';

  return (
    <div className={`task-item ${isCompleted ? 'completed' : ''}`}>
      <div className="task-content">
        <input
          type="checkbox"
          checked={isCompleted}
          onChange={(e) => onToggle(task.id, e.target.checked ? 'completed' : 'pending')}
          className="task-checkbox"
          title="Mark as completed"
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span className="task-text">{task.title || task.description}</span>
          <span className={`badge ${isCompleted ? 'completed' : 'pending'}`}>
             {isCompleted ? 'Completed' : 'Pending'}
          </span>
        </div>
      </div>
      <div className="task-actions">
        <button 
          onClick={() => {
            if (window.confirm("Are you sure you want to delete this task?")) {
              onDelete(task.id);
            }
          }} 
          className="btn-danger"
          title="Delete task"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
