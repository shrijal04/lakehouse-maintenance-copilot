"use client";

import { Bell, Search, UserCircle2 } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 flex h-16 items-center justify-between border-b border-slate-800 bg-slate-950/90 px-8 backdrop-blur">
      <div>
        <h1 className="text-2xl font-bold text-white">
          Lakehouse Maintenance Copilot
        </h1>

        <p className="text-sm text-slate-400">
          Enterprise Data Engineering Dashboard
        </p>
      </div>

      <div className="flex items-center gap-5">
        <Search className="h-5 w-5 cursor-pointer text-slate-400 hover:text-white transition" />

        <Bell className="h-5 w-5 cursor-pointer text-slate-400 hover:text-white transition" />

        <UserCircle2 className="h-8 w-8 cursor-pointer text-slate-300" />
      </div>
    </header>
  );
}