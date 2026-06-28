import { healthSummary } from "@/data/dashboard";

export default function HealthSummary() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Health Summary
      </h2>

      <div className="grid gap-6 md:grid-cols-3">
        {healthSummary.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.id}
              className="rounded-xl bg-slate-800 p-5"
            >
              <Icon
                className={`${item.color} mb-3`}
                size={28}
              />

              <h3 className="font-semibold text-white">
                {item.title}
              </h3>

              <p className="mt-3 text-3xl font-bold text-white">
                {item.value}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}