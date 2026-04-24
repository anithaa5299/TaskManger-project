import { useState } from "react";
import API from "../api";

export default function TaskItem({ task, refresh }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);

  const deleteTask = async () => {
    await API.delete(`/tasks/${task.id}`);
    refresh();
  };

  const updateTask = async () => {
    await API.put(`/tasks/${task.id}`, {
    title: title,
    description: task.description || ""
  });
    setIsEditing(false);
    refresh();
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: 10,
        border: "1px solid #ddd",
        marginBottom: 5
      }}
    >
      {isEditing ? (
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      ) : (
        <span>{task.title}</span>
      )}

      <div>
        {isEditing ? (
          <button onClick={updateTask}>💾 Save</button>
        ) : (
          <button onClick={() => setIsEditing(true)}>✏️ Edit</button>
        )}

        <button onClick={deleteTask} style={{ marginLeft: 5 }}>
          ❌
        </button>
      </div>
    </div>
  );
}