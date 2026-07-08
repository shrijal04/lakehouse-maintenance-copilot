"use client";

import { useState } from "react";
import { FileText, Loader2 } from "lucide-react";

import { generateReport } from "@/services/report";
import ReportDownload from "./ReportDownload";

export default function AIReportCard() {
  const [loading, setLoading] = useState(false);

  const [summary, setSummary] = useState("");

  async function handleGenerate() {
    try {
      setLoading(true);

      const result = await generateReport();

      setSummary(result.summary);
    } catch (err) {
      console.error(err);

      alert("Failed to generate report.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-6 flex items-center gap-3">

        <FileText
          className="text-cyan-400"
          size={28}
        />

        <h2 className="text-2xl font-semibold text-white">
          AI Daily Report
        </h2>

      </div>

      <button
        onClick={handleGenerate}
        disabled={loading}
        className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-black transition hover:bg-cyan-400 disabled:opacity-50"
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <Loader2
              className="animate-spin"
              size={18}
            />
            Generating...
          </span>
        ) : (
          "Generate AI Report"
        )}
      </button>

      {summary && (
        <>
          <div className="mt-8">

            <h3 className="mb-4 text-xl font-semibold text-white">
              AI Summary
            </h3>

            <div className="max-h-96 overflow-auto whitespace-pre-wrap rounded-xl bg-slate-950 p-5 text-sm leading-7 text-slate-300">
              {summary}
            </div>

          </div>

          <ReportDownload />
        </>
      )}

    </div>
  );
}