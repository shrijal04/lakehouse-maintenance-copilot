import { pipelineJobs } from "@/data/pipeline";
import JobStatusBadge from "./JobStatusBadge";

export default function JobTable() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Maintenance Jobs
      </h2>

      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-700 text-left text-slate-400">
            <th className="pb-4">Job</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Last Run</th>
          </tr>
        </thead>

        <tbody>
          {pipelineJobs.map((job) => (
            <tr
              key={job.id}
              className="border-b border-slate-800"
            >
              <td className="py-4 text-white">{job.name}</td>

              <td>
                <JobStatusBadge status={job.status} />
              </td>

              <td className="text-slate-300">
                {job.duration}
              </td>

              <td className="text-slate-300">
                {job.lastRun}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}