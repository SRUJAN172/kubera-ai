import React from "react";
import { NavLink } from "react-router-dom";

function NavItem({ to, icon: Icon, label }) {
  return (
    <NavLink
      to={to}
      end={to === "/"}
      className={({ isActive }) =>
        `flex items-center gap-3 rounded-2xl px-4 py-3 transition-all border ${
          isActive
            ? "bg-white text-[#0B2E24] border-white shadow-sm"
            : "border-transparent text-white/70 hover:text-white hover:bg-white/10"
        }`
      }
    >
      <Icon size={18} />
      <span className="font-medium">{label}</span>
    </NavLink>
  );
}

export default NavItem;