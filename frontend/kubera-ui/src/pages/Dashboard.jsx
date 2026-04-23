import React, { useEffect, useState } from "react";
import { ArrowUpRight, ShieldCheck, Zap } from "lucide-react";
import SpendingPieChart from "../components/charts/SpendingPieChart";
import TrendLineChart from "../components/charts/TrendLineChart";
import SummaryCards from "../components/SummaryCards";
import FinanceBarChart from "../components/charts/FinanceBarCharts";
import InsightsPanel from "../components/InsightsPanel";

function MetricCard({ title, value, icon: Icon, note }) {
  return (
    <div className="col-span-12 md:col-span-4 bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <label className="text-xs uppercase tracking-[0.28em] text-stone-400 font-semibold">
          {title}
        </label>
        <Icon size={18} className="text-[#735C00]" />
      </div>
      <div className="text-4xl mb-2 font-semibold">{value}</div>
      <p className="text-stone-500 text-sm">{note}</p>
    </div>
  );
}

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        const res = await fetch("http://127.0.0.1:8000/analyze");

        if (!res.ok) {
          throw new Error("Failed to fetch dashboard data");
        }

        const result = await res.json();
        setSummary(result.data || null);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  if (loading) {
    return <div className="p-8 text-lg">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-600">Error: {error}</div>;
  }

  if (!summary) {
    return <div className="p-8">No data available.</div>;
  }

  const pieData = summary.category_spending
    ? Object.entries(summary.category_spending).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  const trendMonths = Array.from(
    new Set([
      ...Object.keys(summary.monthly_income_trend || {}),
      ...Object.keys(summary.monthly_expense_trend || {}),
      ...Object.keys(summary.monthly_savings_trend || {}),
    ])
  ).sort();

  const trendData = trendMonths.map((month) => ({
    month,
    income: summary.monthly_income_trend?.[month] || 0,
    expense: summary.monthly_expense_trend?.[month] || 0,
    savings: summary.monthly_savings_trend?.[month] || 0,
  }));

  const barData = [
    { name: "Income", amount: summary.total_income || 0 },
    { name: "Expense", amount: summary.total_expense || 0 },
    { name: "Savings", amount: summary.savings || 0 },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-10">
      <header>
        <h1 className="text-5xl md:text-6xl mb-3 leading-tight font-semibold">
          Good morning, Srujan.
        </h1>
        <p className="text-stone-500 text-lg max-w-2xl">
          Here is your latest financial dashboard from Kubera AI.
        </p>
      </header>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 lg:col-span-8 bg-white rounded-[32px] border border-stone-200 p-8 shadow-sm">
          <label className="text-xs uppercase tracking-[0.28em] text-stone-400 font-semibold">
            Net Savings
          </label>

          <div className="flex items-end gap-3 mt-4 mb-4">
            <span className="text-6xl tracking-tight font-semibold">
              ₹{(summary.savings || 0).toLocaleString()}
            </span>
          </div>

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-50 text-emerald-700 text-sm font-medium">
            <ArrowUpRight size={16} />
            Savings Rate: {summary.savings_rate || 0}%
          </div>

          <p className="text-sm text-stone-500 mt-4">
            Highest spending day: {summary.highest_spending_day?.date || "N/A"} (
            ₹{summary.highest_spending_day?.amount || 0})
          </p>
        </div>

        <div className="col-span-12 lg:col-span-4 bg-[#1A3C34] text-white rounded-[32px] p-8 shadow-sm flex flex-col justify-between">
          <div className="text-center">
            <p className="text-xs uppercase tracking-[0.28em] opacity-60">
              Financial Health
            </p>

            <div className="mt-6">
              <span className="text-5xl font-semibold">
                {summary.savings_rate || 0}%
              </span>
              <p className="text-xs uppercase tracking-[0.28em] opacity-60 mt-2">
                {summary.financial_health || "N/A"}
              </p>
            </div>
          </div>

          <div className="mt-6 text-sm opacity-80 space-y-2">
            <p>Expense ratio: {summary.expense_ratio || 0}%</p>
            <p>Top expense: {summary.highest_expense?.category || "N/A"}</p>
            <p>{summary.budget_warning?.message || "No warning available."}</p>
          </div>
        </div>
      </div>

      <SummaryCards summary={summary} />

      <div className="grid grid-cols-12 gap-6">
        <MetricCard
          title="Transactions"
          value={summary.total_transactions || 0}
          icon={ShieldCheck}
          note="Total tracked"
        />

        <MetricCard
          title="Income Entries"
          value={summary.income_transactions || 0}
          icon={Zap}
          note="Income records"
        />

        <MetricCard
          title="Expense Entries"
          value={summary.expense_transactions || 0}
          icon={ArrowUpRight}
          note="Expense records"
        />

        <MetricCard
          title="Avg Monthly Spend"
          value={`₹${(summary.average_monthly_spending || 0).toLocaleString()}`}
          icon={Zap}
          note="Monthly average"
        />

        <MetricCard
          title="Avg Expense / Txn"
          value={`₹${(
            summary.average_expense_per_transaction || 0
          ).toLocaleString()}`}
          icon={ShieldCheck}
          note="Per expense transaction"
        />

        <MetricCard
          title="Net Cash Flow"
          value={`₹${(summary.net_cash_flow || 0).toLocaleString()}`}
          icon={ArrowUpRight}
          note="Income minus expense"
        />
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 lg:col-span-6 bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm">
          <SpendingPieChart data={pieData} />
        </div>

        <div className="col-span-12 lg:col-span-6 bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm">
          <TrendLineChart data={trendData} />
        </div>

        <div className="col-span-12 lg:col-span-6 bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm">
          <FinanceBarChart data={barData} />
        </div>

        <div className="col-span-12 lg:col-span-6 bg-white rounded-[32px] border border-stone-200 p-7 shadow-sm">
          <InsightsPanel />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;