import React, { useEffect, useState } from "react";
import { apiFetch } from "../utils/api";

function Goals() {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchGoals() {
      try {
        const res = await apiFetch("/goals");

        if (!res.ok) {
          throw new Error("Failed to fetch goals");
        }

        const data = await res.json();
        setGoals(data.data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchGoals();
  }, []);

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-10">
        <h1 className="text-5xl md:text-6xl mb-3 font-semibold">Goals</h1>
        <p className="text-stone-500 text-lg">
          Track your financial milestones with calm precision.
        </p>
      </div>

      {loading ? (
        <p className="text-stone-500">Loading goals...</p>
      ) : error ? (
        <p className="text-red-600">{error}</p>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
          {goals.map((goal) => (
            <div
              key={goal.title}
              className="bg-white border border-stone-200 rounded-[32px] p-8 shadow-sm"
            >
              <p className="text-xs uppercase tracking-[0.28em] text-stone-400 mb-4">
                Goal
              </p>

              <h3 className="text-3xl mb-5 font-semibold">{goal.title}</h3>

              <div className="h-3 bg-stone-100 rounded-full overflow-hidden mb-4">
                <div
                  className="h-full bg-[#1A3C34] rounded-full transition-all duration-500"
                  style={{ width: `${goal.value}%` }}
                />
              </div>

              <div className="flex items-center justify-between">
                <span className="text-2xl font-semibold">
                  {goal.value.toFixed(1)}%
                </span>
                <span className="text-stone-500 text-sm">{goal.amount}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Goals;