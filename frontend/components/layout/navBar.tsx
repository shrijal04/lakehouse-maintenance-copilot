"use client";

import { Bell, Search, UserCircle2 } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 flex h-14 items-center justify-between border-b border-slate-800 bg-slate-950/90 px-6 backdrop-blur">
      <div>
        <h1 className="text-xl font-semibold text-white">
          Lakehouse Maintenance Copilot
        </h1>

        <p className="text-xs text-slate-500">
          Enterprise Data Engineering Dashboard
        </p>
      </div>

      <div className="flex items-center gap-4">
        <Search className="h-5 w-5 cursor-pointer text-slate-400 hover:text-white transition" />

        <Bell className="h-5 w-5 cursor-pointer text-slate-400 hover:text-white transition" />

        <UserCircle2 className="h-7 w-7 cursor-pointer text-slate-300" />
      </div>
    </header>
  );
}