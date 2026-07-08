"use client";

import { Download } from "lucide-react";

const API = "http://127.0.0.1:8000";

export default function ReportDownload() {

  return (
    <div className="mt-8 flex gap-4">

      <a
        href={`${API}/lakehouse/report/pdf`}
        target="_blank"
        rel="noreferrer"
        className="flex items-center gap-2 rounded-xl bg-green-500 px-5 py-3 font-semibold text-black transition hover:bg-green-400"
      >
        <Download size={18} />
        Download PDF
      </a>

      <a
        href={`${API}/lakehouse/report/docx`}
        target="_blank"
        rel="noreferrer"
        className="flex items-center gap-2 rounded-xl bg-blue-500 px-5 py-3 font-semibold text-white transition hover:bg-blue-400"
      >
        <Download size={18} />
        Download DOCX
      </a>

    </div>
  );
}