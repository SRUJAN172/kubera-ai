import React from "react";
import { Search, Filter, Download } from "lucide-react";
import { transactions } from "../data/mockData";

function Transactions() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-10">
        <div>
          <h1 className="text-5xl md:text-6xl mb-3 font-semibold">Transactions</h1>
          <p className="text-stone-500 text-lg">
            Every movement refined, analyzed, and presented clearly.
          </p>
        </div>

        <div className="flex gap-4">
          <button className="flex items-center gap-3 px-6 py-4 bg-white border border-stone-200 rounded-2xl shadow-sm font-medium">
            <Download size={18} />
            Export Journal
          </button>
        </div>
      </div>

      <div className="bg-white rounded-[36px] shadow-sm border border-stone-200 overflow-hidden">
        <div className="p-6 border-b border-stone-100 flex flex-col lg:flex-row gap-4 lg:items-center lg:justify-between">
          <div className="flex-1 relative">
            <Search
              className="absolute left-5 top-1/2 -translate-y-1/2 text-stone-300"
              size={18}
            />
            <input
              className="w-full bg-stone-50 pl-14 pr-5 py-4 rounded-2xl outline-none border border-transparent focus:border-stone-200"
              placeholder="Search by merchant, category, or note"
            />
          </div>

          <button className="px-6 py-4 rounded-2xl border border-stone-200 font-medium flex items-center gap-2">
            Date Range <Filter size={18} className="text-[#735C00]" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left min-w-[760px]">
            <thead>
              <tr className="text-[11px] uppercase tracking-[0.28em] text-stone-400">
                <th className="px-8 py-6">Timestamp</th>
                <th className="px-8 py-6">Beneficiary / Merchant</th>
                <th className="px-8 py-6">Classification</th>
                <th className="px-8 py-6 text-right">Value (USD)</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-stone-100">
              {transactions.map((t, i) => (
                <tr key={i} className="hover:bg-stone-50/70 transition-colors">
                  <td className="px-8 py-6 text-stone-500 font-medium">
                    {t.date}
                  </td>
                  <td className="px-8 py-6 text-xl font-semibold">{t.merchant}</td>
                  <td className="px-8 py-6">
                    <span className="px-4 py-1.5 rounded-full bg-stone-100 text-stone-600 text-xs font-semibold uppercase tracking-[0.14em]">
                      {t.category}
                    </span>
                  </td>
                  <td
                    className={`px-8 py-6 text-right text-2xl font-semibold ${
                      t.amount > 0 ? "text-emerald-700" : "text-stone-800"
                    }`}
                  >
                    {t.amount > 0 ? "+" : ""}
                    {t.amount.toLocaleString("en-US", {
                      style: "currency",
                      currency: "USD",
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Transactions;