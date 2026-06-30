"use client";

import { useEffect, useState } from "react";

import { getIssues } from "@/services/issues";

interface Issue {
  severity: "Healthy" | "Warning" | "Critical";
  issue: string;
  recommendation: string;
}

export default function IssuesTable() {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getIssues()
      .then((data) => {
        setIssues(data);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8 text-white">
        Loading issues...
      </div>
    );
  }

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
      <h2 className="mb-8 text-3xl font-semibold text-white">
        Active Issues
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800 text-left text-slate-400">
              <th className="pb-5 text-base font-semibold">
                Severity
              </th>

              <th className="pb-5 text-base font-semibold">
                Issue
              </th>

              <th className="pb-5 text-base font-semibold">
                Recommendation
              </th>
            </tr>
          </thead>

          <tbody>
            {issues.map((issue, index) => (
              <tr
                key={index}
                className="border-b border-slate-800 transition hover:bg-slate-800/40"
              >
                <td className="py-6">
                  <span
                    className={`rounded-full px-3 py-1 text-sm font-medium
                      ${
                        issue.severity === "Critical"
                          ? "bg-red-500/20 text-red-400"
                          : issue.severity === "Warning"
                          ? "bg-yellow-500/20 text-yellow-400"
                          : "bg-green-500/20 text-green-400"
                      }`}
                  >
                    {issue.severity}
                  </span>
                </td>

                <td className="py-6 text-white">
                  {issue.issue}
                </td>

                <td className="py-6 text-slate-300">
                  {issue.recommendation}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}