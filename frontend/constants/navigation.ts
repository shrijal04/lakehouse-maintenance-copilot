import {
  LayoutDashboard,
  Workflow,
  Database,
  Activity,
  Bot,
  Settings,
} from "lucide-react";

export const navigation = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Pipeline",
    href: "/pipeline",
    icon: Workflow,
  },
  {
    title: "Iceberg",
    href: "/iceberg",
    icon: Database,
  },
  {
    title: "Health",
    href: "/health",
    icon: Activity,
  },
  {
    title: "AI Copilot",
    href: "/copilot",
    icon: Bot,
  },

];