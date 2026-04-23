import React from "react";
import { ArrowUpRight, ArrowDownRight, Wallet, Percent } from "lucide-react";

function Card({ title, value, note, icon: Icon, color }) {
  return (
    <div className="col-span-12 md:col-span-6 xl:col-span-3 bg-white rounded-[32px] border border-stone-200 p-6 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-1">
      
      {/* Top */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-xs uppercase tracking-[0.25em] text-stone-400 font-semibold">
          {title}
        </p>
        <Icon size={18} className={color} />
      </div>

      {/* Value */}
      <h3 className="text-3xl font-semibold mb-2 tracking-tight">
        {value}
      </h3>

      {/* Note */}
      <p className="text-sm text-stone-500">
        {note}
      </p>

    </div>
  );
}

function SummaryCards({ summary }) {
  return (
    <div className="grid grid-cols-12 gap-6">

      <Card
        title="Total Income"
        value={`₹${summary.total_income?.toLocaleString("en-IN") || 0}`}
        note="Money received"
        icon={ArrowUpRight}
        color="text-emerald-600"
      />

      <Card
        title="Total Expense"
        value={`₹${summary.total_expense?.toLocaleString("en-IN") || 0}`}
        note="Money spent"
        icon={ArrowDownRight}
        color="text-red-500"
      />

      <Card
        title="Savings"
        value={`₹${summary.savings?.toLocaleString("en-IN") || 0}`}
        note="Income minus expense"
        icon={Wallet}
        color="text-[#735C00]"
      />

      <Card
        title="Savings Rate"
        value={`${summary.savings_rate || 0}%`}
        note="Portion of income saved"
        icon={Percent}
        color="text-[#1A3C34]"
      />

    </div>
  );
}

export default SummaryCards;