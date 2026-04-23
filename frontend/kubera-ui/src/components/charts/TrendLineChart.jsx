import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function TrendLineChart({ data = [] }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Monthly Trend</h2>

      {data.length === 0 ? (
        <p className="text-stone-500">No trend data available.</p>
      ) : (
        <div className="w-full h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="income" stroke="#16a34a" strokeWidth={3} />
              <Line type="monotone" dataKey="expense" stroke="#dc2626" strokeWidth={3} />
              <Line type="monotone" dataKey="savings" stroke="#2563eb" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default TrendLineChart;