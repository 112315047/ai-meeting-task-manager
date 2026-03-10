import React from 'react';
import TaskItem from './TaskItem';

const TaskList = ({ tasks, onToggleTask, onDeleteTask, loading, error }) => {
  if (loading) {
    return <div className="loading-state">Loading tasks...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  if (!tasks || tasks.length === 0) {
    return <div className="text-center mt-4 mb-4" style={{color: '#6b7280'}}>No tasks found. Create one above!</div>;
  }

  return (
    <div className="task-list">
      {tasks.map(task => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onToggle={onToggleTask}
          onDelete={onDeleteTask}
        />
      ))}
    </div>
  );
};

export default TaskList;
