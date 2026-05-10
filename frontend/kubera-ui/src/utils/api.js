const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("kubera_token");

  const headers = { ...options.headers };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Don't set Content-Type for FormData (browser sets it with boundary)
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  // Auto-logout on 401
  if (res.status === 401) {
    localStorage.removeItem("kubera_token");
    localStorage.removeItem("kubera_user");
    window.location.href = "/login";
    throw new Error("Session expired. Please login again.");
  }

  return res;
}

export default API_BASE;
