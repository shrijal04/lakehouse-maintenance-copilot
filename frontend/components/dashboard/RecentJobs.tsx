import StatusBadge from "./StatusBadge";

interface Job {
  id: number;
  job: string;
  status: string;
  duration: string;
  time: string;
}

interface Props {
  jobs: Job[];
}

export default function RecentJobs({ jobs }: Props) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Recent Maintenance Jobs
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-slate-800 text-left text-slate-400">
            <tr>
              <th className="pb-3">Job</th>
              <th className="pb-3">Status</th>
              <th className="pb-3">Duration</th>
              <th className="pb-3">Time</th>
            </tr>
          </thead>

          <tbody>
            {jobs.map((job) => (
              <tr
                key={job.id}
                className="border-b border-slate-800 last:border-none"
              >
                <td className="py-4 text-white">{job.job}</td>

                <td>
                  <StatusBadge status={job.status} />
                </td>

                <td className="text-slate-300">{job.duration}</td>

                <td className="text-slate-300">{job.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}