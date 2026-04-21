import React from "react";
import { ArrowUpRight, ShieldCheck, Zap } from "lucide-react";

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
  return (
    <div className="max-w-7xl mx-auto space-y-10">
      <header>
        <h1 className="text-5xl md:text-6xl mb-3 leading-tight font-semibold">
          Good morning, Srujan.
        </h1>
        <p className="text-stone-500 text-lg max-w-2xl">
          Your financial landscape is stable, with healthy momentum in savings
          and investments.
        </p>
      </header>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 lg:col-span-8 bg-white rounded-[40px] border border-stone-200 p-8 md:p-10 shadow-sm">
          <label className="text-xs uppercase tracking-[0.28em] text-stone-400 font-semibold">
            Net Worth
          </label>

          <div className="flex items-end gap-3 mt-4 mb-8">
            <span className="text-6xl md:text-7xl tracking-tight font-semibold">
              $2,845,920
            </span>
            <span className="text-2xl text-stone-300 mb-2">.00</span>
          </div>

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-50 text-emerald-700 text-sm font-medium mb-8">
            <ArrowUpRight size={16} />
            +12.4% vs last quarter
          </div>

          <div className="h-48 rounded-[28px] bg-gradient-to-br from-stone-50 to-stone-100 border border-stone-200 flex items-end justify-between p-6 overflow-hidden">
            {[45, 70, 56, 92, 76, 105, 98, 120].map((h, i) => (
              <div
                key={i}
                className="w-8 md:w-10 rounded-t-2xl bg-[#1A3C34]"
                style={{ height: `${h}px`, opacity: 0.35 + i * 0.07 }}
              />
            ))}
          </div>
        </div>

        <div className="col-span-12 lg:col-span-4 bg-[#1A3C34] text-white rounded-[40px] p-8 shadow-sm flex flex-col justify-between">
          <div>
            <label className="text-xs uppercase tracking-[0.28em] opacity-60 font-semibold">
              Health Index
            </label>

            <div className="relative w-52 h-52 mx-auto my-8">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 220 220">
                <circle
                  cx="110"
                  cy="110"
                  r="88"
                  fill="transparent"
                  stroke="rgba(255,255,255,0.15)"
                  strokeWidth="18"
                />
                <circle
                  cx="110"
                  cy="110"
                  r="88"
                  fill="transparent"
                  stroke="#735C00"
                  strokeWidth="18"
                  strokeDasharray="553"
                  strokeDashoffset="99"
                  strokeLinecap="round"
                />
              </svg>

              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-5xl font-semibold">82%</span>
                <span className="text-xs uppercase tracking-[0.28em] opacity-60 mt-2">
                  Excellent
                </span>
              </div>
            </div>
          </div>

          <p className="text-sm opacity-75 italic leading-7">
            Your liquidity, savings rhythm, and income stability indicate a
            strong financial profile.
          </p>
        </div>

        <MetricCard
          title="Protected Assets"
          value="12"
          icon={ShieldCheck}
          note="Accounts monitored"
        />
        <MetricCard
          title="Active Budget Rules"
          value="08"
          icon={Zap}
          note="Automations running"
        />
        <MetricCard
          title="Monthly Savings"
          value="$4,240"
          icon={ArrowUpRight}
          note="Ahead of target"
        />
      </div>
    </div>
  );
}

export default Dashboard;