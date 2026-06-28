import { issues } from "@/data/health";

export default function IssuesTable() {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
      <h2 className="mb-8 text-3xl font-semibold text-white">
        Active Issues
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800 text-left text-slate-400">
              <th className="w-1/5 pb-5 text-base font-semibold">
                Table
              </th>

              <th className="w-1/5 pb-5 text-base font-semibold">
                Severity
              </th>

              <th className="w-2/5 pb-5 text-base font-semibold">
                Issue
              </th>

              <th className="w-1/5 pb-5 text-center text-base font-semibold">
                Action
              </th>
            </tr>
          </thead>

          <tbody>
            {issues.map((issue) => (
              <tr
                key={issue.id}
                className="border-b border-slate-800 hover:bg-slate-800/40 transition"
              >
                <td className="py-7 font-medium text-white">
                  {issue.table}
                </td>

                <td className="py-7">
                  <span
                    className={`rounded-full px-3 py-1 text-sm font-medium ${
                      issue.severity === "Critical"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-yellow-500/20 text-yellow-400"
                    }`}
                  >
                    {issue.severity}
                  </span>
                </td>

                <td className="py-7 text-slate-300">
                  {issue.issue}
                </td>

                <td className="py-7 text-center">
                  <button className="rounded-xl bg-cyan-500 px-5 py-2 text-sm font-semibold text-black transition hover:bg-cyan-400">
                    {issue.action}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}