const API_BASE = "http://127.0.0.1:5000";

export async function fetchTasks() {
  const res = await fetch(`${API_BASE}/tasks`);
  if (!res.ok) throw new Error("Backend connection failed");

  const data = await res.json();
  return data.tasks;
}

export async function extractTasks(notes) {
  const res = await fetch(`${API_BASE}/tasks/extract`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notes })
  });

  if (!res.ok) throw new Error("Extract failed");

  return res.json();
}

export async function createTask(task) {
  const res = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task)
  });

  if (!res.ok) throw new Error("Create failed");

  return res.json();
}

export async function updateTaskStatus(id, status) {
  const res = await fetch(`${API_BASE}/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });

  if (!res.ok) throw new Error("Update failed");

  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${API_BASE}/tasks/${id}`, {
    method: "DELETE"
  });

  if (!res.ok) throw new Error("Delete failed");

  return res.json();
}
