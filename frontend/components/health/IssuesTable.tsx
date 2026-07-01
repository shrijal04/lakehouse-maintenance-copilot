"use client";

import { useEffect, useState } from "react";

import {
  getIssues,
  getOrderItemsIssues,
} from "@/services/issues";

interface Issue {
  severity: "Healthy" | "Warning" | "Critical";
  issue: string;
  recommendation: string;
}

export default function IssuesTable() {
  const [ordersIssues, setOrdersIssues] = useState<Issue[]>([]);
  const [orderItemsIssues, setOrderItemsIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [orders, orderItems] = await Promise.all([
          getIssues(),
          getOrderItemsIssues(),
        ]);

        setOrdersIssues(orders);
        setOrderItemsIssues(orderItems);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8 text-white">
        Loading issues...
      </div>
    );
  }

  function renderTable(title: string, issues: Issue[]) {
    return (
      <div className="mb-10">
        <h3 className="mb-4 text-xl font-semibold text-cyan-400">
          {title}
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800 text-left text-slate-400">
                <th className="pb-4">Severity</th>
                <th className="pb-4">Issue</th>
                <th className="pb-4">Recommendation</th>
              </tr>
            </thead>

            <tbody>
              {issues.map((issue, index) => (
                <tr
                  key={index}
                  className="border-b border-slate-800 hover:bg-slate-800/40"
                >
                  <td className="py-5">
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

                  <td className="py-5 text-white">
                    {issue.issue}
                  </td>

                  <td className="py-5 text-slate-300">
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

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
      <h2 className="mb-8 text-3xl font-semibold text-white">
        Active Issues
      </h2>

      {renderTable("Orders", ordersIssues)}

      {renderTable("Order Items", orderItemsIssues)}
    </div>
  );
}