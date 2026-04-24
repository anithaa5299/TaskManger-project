import { useState } from "react";
import API from "../api";

export default function Login({ setToken }) {
  const [isLogin, setIsLogin] = useState(true);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    try {
      if (isLogin) {
        // LOGIN
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const res = await API.post("/login", formData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        });

        localStorage.setItem("token", res.data.access_token);
        setToken(res.data.access_token);
      } else {
        // REGISTER
        await API.post("/register", {
          email,
          password,
        });

        alert("User registered! Now login.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error(err);
      alert(isLogin ? "Login failed" : "Register failed");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>{isLogin ? "🔐 Login" : "📝 Register"}</h2>

      <input
        placeholder="email"
        onChange={(e) => setEmail(e.target.value)}
        style={{ display: "block", marginBottom: 10 }}
      />

      <input
        type="password"
        placeholder="password"
        onChange={(e) => setPassword(e.target.value)}
        style={{ display: "block", marginBottom: 10 }}
      />

      <button onClick={submit}>
        {isLogin ? "Login" : "Register"}
      </button>

      <p
        style={{ marginTop: 10, cursor: "pointer", color: "blue" }}
        onClick={() => setIsLogin(!isLogin)}
      >
        {isLogin
          ? "No account? Register here"
          : "Already have account? Login"}
      </p>
    </div>
  );
}