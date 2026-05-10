import React, { createContext, useContext, useState, useEffect } from "react";
import { apiFetch } from "../utils/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("kubera_token"));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      apiFetch("/me")
        .then((res) => {
          if (!res.ok) throw new Error("Invalid token");
          return res.json();
        })
        .then((data) => {
          setUser(data.user);
        })
        .catch(() => {
          localStorage.removeItem("kubera_token");
          localStorage.removeItem("kubera_user");
          setToken(null);
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    const res = await apiFetch("/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login failed");
    }

    localStorage.setItem("kubera_token", data.token);
    localStorage.setItem("kubera_user", JSON.stringify(data.user));
    setToken(data.token);
    setUser(data.user);

    return data;
  };

  const register = async (name, email, password) => {
    const res = await apiFetch("/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Registration failed");
    }

    localStorage.setItem("kubera_token", data.token);
    localStorage.setItem("kubera_user", JSON.stringify(data.user));
    setToken(data.token);
    setUser(data.user);

    return data;
  };

  const logout = () => {
    localStorage.removeItem("kubera_token");
    localStorage.removeItem("kubera_user");
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = !!token && !!user;

  return (
    <AuthContext.Provider
      value={{ user, token, login, register, logout, isAuthenticated, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default AuthContext;
