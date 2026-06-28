import QuickActionButton from "./QuickActionButton";
import { quickActions } from "@/data/dashboard";

export default function QuickActions() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Quick Actions
      </h2>

      <div className="grid gap-4 md:grid-cols-2">
        {quickActions.map((action) => (
          <QuickActionButton
            key={action.id}
            title={action.title}
            description={action.description}
          />
        ))}
      </div>
    </div>
  );
}