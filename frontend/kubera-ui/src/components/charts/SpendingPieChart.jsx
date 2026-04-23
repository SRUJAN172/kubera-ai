import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = ["#1A3C34", "#735C00", "#D6C7A1", "#A67C52", "#5B8C85"];

function SpendingPieChart({ data = [] }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Category Spending</h2>

      {data.length === 0 ? (
        <p className="text-stone-500">No spending data available.</p>
      ) : (
        <div className="w-full h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                cx="50%"
                cy="50%"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default SpendingPieChart;