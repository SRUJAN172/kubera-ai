import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { LogIn, Eye, EyeOff } from "lucide-react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password.trim()) {
      setError("Please fill in all fields");
      return;
    }

    setLoading(true);

    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F9F8F4] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl tracking-[0.12em] uppercase text-[#735C00] mb-3">
            Kubera AI
          </h1>
          <p className="text-stone-500 text-lg">
            Welcome back to your financial workspace
          </p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-[32px] border border-stone-200 p-8 md:p-10 shadow-sm">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-11 h-11 rounded-2xl bg-[#1A3C34] text-white flex items-center justify-center">
              <LogIn size={20} />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-[#1A3C34]">Sign In</h2>
              <p className="text-sm text-stone-500">
                Access your financial dashboard
              </p>
            </div>
          </div>

          {error && (
            <div className="mb-6 px-4 py-3 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs uppercase tracking-[0.25em] text-stone-400 font-semibold mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full bg-stone-50 px-5 py-4 rounded-2xl outline-none border border-transparent focus:border-stone-200 text-[#1A3C34]"
                autoComplete="email"
              />
            </div>

            <div>
              <label className="block text-xs uppercase tracking-[0.25em] text-stone-400 font-semibold mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-stone-50 px-5 py-4 rounded-2xl outline-none border border-transparent focus:border-stone-200 text-[#1A3C34] pr-12"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-600"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#1A3C34] text-white py-4 rounded-2xl font-semibold text-lg hover:bg-[#0c2920] transition-colors disabled:opacity-50 mt-2"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <p className="text-center text-stone-500 text-sm mt-6">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="text-[#735C00] font-semibold hover:underline"
            >
              Create one
            </Link>
          </p>
        </div>

        <p className="text-center text-stone-400 text-xs mt-8">
          Secure. Elegant. Intelligent.
        </p>
      </div>
    </div>
  );
}

export default Login;
