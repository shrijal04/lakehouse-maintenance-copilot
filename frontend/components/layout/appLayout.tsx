import { ReactNode } from "react";
import Sidebar from "./sidebar";
import Navbar from "./navBar";

interface AppLayoutProps {
  children: ReactNode;
}

export default function AppLayout({
  children,
}: AppLayoutProps) {
  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />

      <div className="flex flex-1 flex-col">
        <Navbar />

        <main className="flex-1 px-6 py-5 overflow-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}