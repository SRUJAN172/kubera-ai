import React, { useEffect, useState } from "react";
import { CreditCard, Zap, CalendarClock } from "lucide-react";
import { apiFetch } from "../utils/api";

function Subscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [totalCost, setTotalCost] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSubscriptions() {
      try {
        const res = await apiFetch("/subscriptions");

        if (!res.ok) {
          throw new Error("Failed to fetch subscriptions");
        }

        const data = await res.json();
        setSubscriptions(data.subscriptions || []);
        setTotalCost(data.total_monthly_cost || 0);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    }

    fetchSubscriptions();
  }, []);

  if (loading) {
    return <div className="max-w-7xl mx-auto p-8">Loading your subscriptions...</div>;
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto p-8 text-red-600">Error: {error}</div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-10">
      <header>
        <h1 className="text-5xl md:text-6xl mb-3 leading-tight font-semibold">
          Subscriptions
        </h1>
        <p className="text-stone-500 text-lg max-w-2xl">
          Kubera AI automatically detects your recurring payments and bills.
        </p>
      </header>

      <div className="bg-[#1A3C34] text-white rounded-[32px] p-8 shadow-sm flex flex-col justify-between max-w-md">
        <div className="text-left">
          <p className="text-xs uppercase tracking-[0.28em] opacity-60 flex items-center gap-2">
            <Zap size={14} /> Total Monthly Cost
          </p>

          <div className="mt-6">
            <span className="text-5xl font-semibold">
              ₹{totalCost.toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {subscriptions.length > 0 ? (
          subscriptions.map((sub, index) => (
            <div
              key={index}
              className="bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="p-3 bg-[#F9F8F4] rounded-2xl">
                  <CreditCard className="text-[#735C00]" size={24} />
                </div>
                <span className="text-xs font-semibold uppercase tracking-wider text-stone-400 bg-stone-100 px-3 py-1 rounded-full">
                  {sub.count} Payments
                </span>
              </div>
              <h2 className="text-2xl font-semibold mb-2">{sub.name}</h2>
              <div className="flex items-end gap-2 mb-4">
                <span className="text-3xl font-semibold">
                  ₹{sub.amount.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                </span>
                <span className="text-stone-500 mb-1">/ occurrence</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-stone-500 border-t border-stone-100 pt-4 mt-2">
                <CalendarClock size={16} />
                Last Billed: {sub.last_date}
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-stone-500 bg-white rounded-[32px] border border-stone-200">
            No recurring subscriptions detected yet. Keep logging your expenses!
          </div>
        )}
      </div>
    </div>
  );
}

export default Subscriptions;
