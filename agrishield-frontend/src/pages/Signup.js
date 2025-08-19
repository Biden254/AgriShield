import { useState } from "react";
import { signup } from "../services/authService";
import "../styles/auth.css";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password1: "",
    password2: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Simple client-side password check
    if (formData.password1 !== formData.password2) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await signup(formData);
      setSuccess("Account created successfully! You can now log in.");
      setFormData({
        username: "",
        email: "",
        password1: "",
        password2: "",
      });
    } catch (err) {
      // Handle backend-specific errors more cleanly
      if (err.response?.data) {
        const data = err.response.data;
        setError(
          data.username?.[0] ||
          data.email?.[0] ||
          data.password1?.[0] ||
          data.non_field_errors?.[0] ||
          "Signup failed. Please try again."
        );
      } else {
        setError("Signup failed. Please try again.");
      }
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
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
          name="password1"
          placeholder="Password"
          value={formData.password1}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password2"
          placeholder="Confirm Password"
          value={formData.password2}
          onChange={handleChange}
          required
        />
        <button type="submit">Sign Up</button>
        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
