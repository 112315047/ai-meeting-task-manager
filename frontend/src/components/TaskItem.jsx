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
        <span className="task-text">{task.title || task.description}</span>
      </div>
      <div className="task-actions">
        <button 
          onClick={() => onDelete(task.id)} 
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
