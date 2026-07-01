import {
  LayoutDashboard,
  Workflow,
  Database,
  Activity,
  Bot,
  Wrench,
} from "lucide-react";

export const navigation = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Incremental Load",
    href: "/incremental",
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
    title: "Maintenance",
    href: "/maintenance",
    icon: Wrench,
  },
  {
    title: "AI Copilot",
    href: "/copilot",
    icon: Bot,
  },
];