import { useState } from "react";
import useAuth from "../hooks/useAuth";
import "../styles/auth.css";

export default function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const { login, error, loading } = useAuth();
  const [localError, setLocalError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError("");

    const success = await login(formData);
    if (success) {
      window.location.href = "/dashboard"; // Redirect on success
    } else {
      setLocalError("Invalid email or password.");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Login</h2>

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        {(localError || error) && (
          <p className="error">{localError || error}</p>
        )}
      </form>
    </div>
  );
}
