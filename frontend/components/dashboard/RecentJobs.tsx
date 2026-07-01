import StatusBadge from "./StatusBadge";

interface Job {
  finished_at: string;
  status: string;
  duration_seconds: number;
  files_rewritten: number;
}

interface Props {
  jobs: Job[];
}

export default function RecentJobs({ jobs }: Props) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Maintenance History
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-800 text-left text-slate-400">
            <tr>
              <th className="pb-3">Finished At</th>
              <th className="pb-3">Status</th>
              <th className="pb-3">Duration</th>
              <th className="pb-3">Files Rewritten</th>
            </tr>
          </thead>

          <tbody>
            {jobs.map((job, index) => (
              <tr
                key={index}
                className="border-b border-slate-800 last:border-none"
              >
                <td className="py-4 text-white">
                  {new Date(job.finished_at).toLocaleString()}
                </td>

                <td>
                  <StatusBadge status={job.status} />
                </td>

                <td className="text-slate-300">
                  {job.duration_seconds}s
                </td>

                <td className="text-slate-300">
                  {job.files_rewritten}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}