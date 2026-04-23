import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function FinanceBarChart({ data = []}) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Financial Comparison</h2>

      {data.length === 0 ? (
        <p className="text-stone-500">No bar chart data available.</p>
      ) : (
        <BarChart width={500} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />

          <Bar dataKey="amount" fill="#1A3C34" radius={[10, 10, 0, 0]} />
        </BarChart>
      )}
    </div>
  );
}

export default FinanceBarChart;