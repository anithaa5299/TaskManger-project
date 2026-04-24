import { useEffect, useState } from "react";
import API from "../api";
import TaskItem from "../components/TaskItem";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const res = await API.get("/tasks");
      setTasks(res.data);
    } catch (err) {
      alert("Failed to fetch tasks");
    }
    setLoading(false);
  };

  const createTask = async () => {
    if (!title) return;

    await API.post("/tasks", {
      title,
      description: ""
    });

    setTitle("");
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h2>📋 Task Manager</h2>

      <div style={{ marginBottom: 10 }}>
        <input
          value={title}
          placeholder="Enter task..."
          onChange={(e) => setTitle(e.target.value)}
          style={{ padding: 8, marginRight: 10 }}
        />
        <button onClick={createTask}>➕ Add</button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            refresh={fetchTasks}
          />
        ))
      )}
    </div>
  );
}