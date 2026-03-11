import React, { useState, useEffect, useCallback } from 'react';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import NotesExtractor from './components/NotesExtractor';
import { fetchTasks, extractTasks, createTask, updateTaskStatus, deleteTask } from './services/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('list'); // 'list' or 'extract'
  const [filter, setFilter] = useState('All'); // 'All', 'Pending', 'Completed'

  const loadTasks = async () => {
    try {
      const tasks = await fetchTasks();
      setTasks(tasks);
      setLoading(false);
    } catch (err) {
      console.error("Failed to load tasks:", err);
      setError("Failed to connect to the backend");
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/health")
      .then(r => r.json())
      .then(data => console.log("Backend OK:", data))
      .catch(err => console.error("Backend unreachable:", err));
  }, []);

  const handleCreateTask = async (taskData) => {
    try {
      await createTask(taskData);
      await loadTasks();
      return true;
    } catch (err) {
      alert('Failed to create task');
      console.error(err);
      return false;
    }
  };

  const handleToggleTask = async (id, status) => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, status } : t));
    try {
      await updateTaskStatus(id, status);
    } catch (err) {
      await loadTasks();
      alert('Failed to update task');
      console.error(err);
    }
  };

  const handleDeleteTask = async (id) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    setTasks(prev => prev.filter(t => t.id !== id));
    try {
      await deleteTask(id);
    } catch (err) {
      await loadTasks();
      alert('Failed to delete task');
      console.error(err);
    }
  };

  const handleExtractTasks = async (notes) => {
    try {
      await extractTasks(notes);
      await loadTasks();
      setActiveTab('list');
    } catch (err) {
      console.error(err);
      throw err;
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>AI Task Manager</h1>
        <p style={{color: '#6b7280'}}>Manage your tasks or extract them instantly from meeting notes.</p>
      </header>

      <div className="tabs">
        <button 
          className={activeTab === 'list' ? 'active' : ''} 
          onClick={() => setActiveTab('list')}
        >
          My Tasks
        </button>
        <button 
          className={activeTab === 'extract' ? 'active' : ''} 
          onClick={() => setActiveTab('extract')}
        >
          Extract Tasks
        </button>
      </div>

      <main>
        {activeTab === 'list' && (
          <>
            <TaskForm onTaskCreate={handleCreateTask} />
            <div className="card pt-0">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ margin: 0 }}>Task List</h2>
                <button onClick={loadTasks} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>
                  Refresh
                </button>
              </div>
              
              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
                <button 
                  className={filter === 'All' ? 'btn-primary' : ''} 
                  onClick={() => setFilter('All')}
                >All</button>
                <button 
                  className={filter === 'Pending' ? 'btn-primary' : ''} 
                  onClick={() => setFilter('Pending')}
                >Pending</button>
                <button 
                  className={filter === 'Completed' ? 'btn-primary' : ''} 
                  onClick={() => setFilter('Completed')}
                >Completed</button>
              </div>

              <TaskList 
                tasks={tasks.filter(t => filter === 'All' ? true : (filter === 'Completed' ? t.status === 'completed' : t.status === 'pending'))} 
                loading={loading} 
                error={error} 

                onToggleTask={handleToggleTask} 
                onDeleteTask={handleDeleteTask} 
              />
            </div>
          </>
        )}

        {activeTab === 'extract' && (
          <NotesExtractor onExtractTasks={handleExtractTasks} />
        )}
      </main>
    </div>
  );
}

export default App;
