import { useState } from "react";
import Login from "./pages/Login";
import Tasks from "./pages/Tasks";


function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
  <div>
    {/* Tailwind test */}
    <div className="bg-red-500 text-white p-4">
      Tailwind is working 🚀
    </div>

    {token ? (
      <>
        <button onClick={logout}>🚪 Logout</button>
        <Tasks />
      </>
    ) : (
      <Login setToken={setToken} />
    )}
  </div>
);
}

export default App;