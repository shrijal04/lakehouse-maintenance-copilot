"use client";

import Logo from "@/components/common/logo";
import SidebarItem from "./sidebarItem";
import { navigation } from "@/constants/navigation";

export default function Sidebar() {
  return (
    <aside className="sticky top-0 flex min-h-screen w-72 flex-col border-r border-slate-800 bg-slate-950">
      <div className="border-b border-slate-800 p-6">
        <Logo />
      </div>

      <nav className="flex flex-1 flex-col gap-2 p-4">
        {navigation.map((item) => (
          <SidebarItem
            key={item.title}
            title={item.title}
            href={item.href}
            icon={item.icon}
          />
        ))}
      </nav>
    </aside>
  );
}