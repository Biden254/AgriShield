import api from "../config/api";

// Signup
export const signup = async (data) => {
  return await api.post("/api/auth/registration/", data);
};

// Login
export const login = async (data) => {
  const response = await api.post("/api/auth/login/", data);

  // Save token
  localStorage.setItem("authToken", response.data.key);

  return response;
};

// Logout
export const logout = async () => {
  const token = localStorage.getItem("authToken");
  if (token) {
    await api.post("/api/auth/logout/", {}, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    localStorage.removeItem("authToken");
  }
};

// Get logged-in user
export const getUser = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) throw new Error("No authentication token found");

  const response = await api.get("/api/auth/user/", {
    headers: {
      Authorization: `Token ${token}`,
    },
  });

  return response.data;
};
