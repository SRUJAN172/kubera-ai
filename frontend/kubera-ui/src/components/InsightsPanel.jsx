import React, { useEffect, useState } from "react";
import {
  Sparkles,
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  XCircle,
} from "lucide-react";

const API_BASE = "http://127.0.0.1:8000";

function getInsightType(text = "") {
  const lower = text.toLowerCase();

  if (
    lower.includes("deficit") ||
    lower.includes("overspending") ||
    lower.includes("negative") ||
    lower.includes("warning sign") ||
    lower.includes("attention") ||
    lower.includes("very large portion")
  ) {
    return "danger";
  }

  if (
    lower.includes("high") ||
    lower.includes("reduce") ||
    lower.includes("moderately") ||
    lower.includes("consider") ||
    lower.includes("below") ||
    lower.includes("needs attention")
  ) {
    return "warning";
  }

  return "good";
}

function getInsightStyles(type) {
  if (type === "danger") {
    return {
      wrapper: "border-red-200 bg-red-50",
      iconColor: "text-red-600",
      textColor: "text-red-900",
      icon: <XCircle size={18} />,
      label: "Risk",
    };
  }

  if (type === "warning") {
    return {
      wrapper: "border-yellow-200 bg-yellow-50",
      iconColor: "text-yellow-600",
      textColor: "text-yellow-900",
      icon: <AlertTriangle size={18} />,
      label: "Warning",
    };
  }

  return {
    wrapper: "border-emerald-200 bg-emerald-50",
    iconColor: "text-emerald-600",
    textColor: "text-emerald-900",
    icon: <CheckCircle2 size={18} />,
    label: "Good",
  };
}

function InsightsPanel() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchInsights() {
      try {
        setLoading(true);
        setError("");

        const res = await fetch(`${API_BASE}/insights`);

        if (!res.ok) {
          throw new Error(`Failed to fetch insights (${res.status})`);
        }

        const data = await res.json();
        setInsights(Array.isArray(data.insights) ? data.insights : []);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    }

    fetchInsights();
  }, []);

  return (
    <div>
      <div className="flex items-center gap-3 mb-5">
        <div className="w-11 h-11 rounded-2xl bg-[#1A3C34] text-white flex items-center justify-center">
          <Sparkles size={20} />
        </div>

        <div>
          <h2 className="text-xl font-semibold">Insights</h2>
          <p className="text-sm text-stone-500">
            Financial observations generated from your data.
          </p>
        </div>
      </div>

      {loading ? (
        <p className="text-stone-500">Loading insights...</p>
      ) : error ? (
        <div className="flex items-center gap-2 text-red-600">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      ) : insights.length === 0 ? (
        <p className="text-stone-500">No insights available.</p>
      ) : (
        <div className="space-y-4">
          {insights.map((insight, index) => {
            const type = getInsightType(insight);
            const styles = getInsightStyles(type);

            return (
              <div
                key={`${index}-${insight.slice(0, 20)}`}
                className={`rounded-2xl border p-4 ${styles.wrapper}`}
              >
                <div className="flex items-start gap-3">
                  <div className={`mt-0.5 ${styles.iconColor}`}>
                    {styles.icon}
                  </div>

                  <div className="flex-1">
                    <p
                      className={`text-[11px] uppercase tracking-[0.22em] font-semibold mb-2 ${styles.iconColor}`}
                    >
                      {styles.label}
                    </p>
                    <p className={`${styles.textColor} leading-7`}>
                      {insight}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default InsightsPanel;