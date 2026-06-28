import { maintenanceHistory } from "@/data/health";

export default function MaintenanceHistory() {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">

      <h2 className="mb-6 text-2xl font-semibold text-white">
        Maintenance History
      </h2>

      <div className="space-y-5">

        {maintenanceHistory.map((item) => (

          <div
            key={item.id}
            className="flex items-center justify-between rounded-xl bg-slate-800 p-4"
          >

            <div>

              <p className="font-semibold text-white">
                {item.job}
              </p>

              <p className="text-sm text-slate-400">
                {item.time}
              </p>

            </div>

            <span className="rounded-full bg-green-500/20 px-3 py-1 text-green-400">
              {item.status}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}