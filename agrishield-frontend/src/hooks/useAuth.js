import { useState, useEffect, useCallback } from "react";
import {
  signup as signupService,
  login as loginService,
  logout as logoutService,
  getUser as getUserService,
} from "../services/authService";

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch current logged-in user
  const fetchUser = useCallback(async () => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      const response = await getUserService();
      setUser(response.data);
    } catch (err) {
      setUser(null);
      localStorage.removeItem("authToken");
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-fetch user on mount
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Signup new user
  const signup = async (formData) => {
    setError(null);
    try {
      await signupService(formData);
      // Automatically login after signup
      const loginResponse = await loginService({
        username: formData.username,
        password: formData.password1,
      });
      localStorage.setItem("authToken", loginResponse.data.key);
      await fetchUser();
      return true;
    } catch (err) {
      setError(
        err.response?.data?.username?.[0] ||
          err.response?.data?.email?.[0] ||
          err.response?.data?.password1?.[0] ||
          err.response?.data?.non_field_errors?.[0] ||
          "Signup failed. Please try again."
      );
      return false;
    }
  };

  // Login existing user
  const login = async (formData) => {
    setError(null);
    try {
      const response = await loginService(formData);
      localStorage.setItem("authToken", response.data.key);
      await fetchUser();
      return true;
    } catch (err) {
      setError(
        err.response?.data?.non_field_errors?.[0] ||
          "Invalid username or password."
      );
      return false;
    }
  };

  // Logout user
  const logout = async () => {
    try {
      await logoutService();
    } finally {
      localStorage.removeItem("authToken");
      setUser(null);
    }
  };

  return {
    user,
    loading,
    error,
    signup,
    login,
    logout,
  };
}
