import React from "react";
import logo from "../../assets/logo.png";

import {
  ShieldCheck,
  LayoutDashboard,
  MessageSquare,
  Receipt,
  Target,
} from "lucide-react";
import NavItem from "./NavItem";

function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-[#F9F8F4] text-[#1A3C34] flex">
      <aside className="hidden md:flex w-72 border-r border-stone-200 bg-[#0c2920] flex-col px-6 py-8">
        <div className="mb-10 flex items-center gap-3">
         <img src={logo} alt="Kubera AI Logo" className="h-12 w-12 object-contain" />
          <div>
            <p className="text-white/60">Kubera AI</p>
            <h1 className="text-white">Financial Atelier</h1>
          </div>
        </div>

        <nav className="space-y-2">
          <NavItem to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
          <NavItem to="/" icon={MessageSquare} label="Chat" />
          <NavItem to="/transactions" icon={Receipt} label="Transactions" />
          <NavItem to="/goals" icon={Target} label="Goals" />
        </nav>

        <div className="mt-auto rounded-[28px] bg-[#1A3C34] p-5 text-white shadow-sm">
          <p className="text-xs uppercase tracking-[0.22em] text-white/60 mb-2">
            Private Finance
          </p>
          <h3 className="text-2xl mb-2 font-semibold">
            Secure. Elegant. Intelligent.
          </h3>
          <p className="text-sm text-white/70 leading-6">
            Your financial data stays organized in a calm, premium workspace.
          </p>
        </div>
      </aside>

      <div className="flex-1 min-w-0 flex flex-col">
        <header className="h-20 border-b border-stone-200 bg-[#F9F8F4]/90 px-6 lg:px-10 flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-stone-500">
              Personal Finance Intelligence
            </p>
            <h2 className="text-2xl font-semibold">Kubera AI</h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-full border border-stone-200 bg-white text-sm text-stone-500">
              <ShieldCheck size={16} className="text-[#735C00]" />
              Secured Workspace
            </div>

            <div className="h-11 w-11 rounded-full bg-[#1A3C34] text-white flex items-center justify-center font-semibold">
              S
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto px-6 py-8 lg:px-10 lg:py-10">
          {children}
        </main>
      </div>
    </div>
  );
}

export default AppShell;