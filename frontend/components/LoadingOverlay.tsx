"use client";

export default function LoadingOverlay() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm">
      <div className="text-center">

        <div className="mx-auto h-16 w-16 animate-spin rounded-full border-4 border-slate-500 border-t-cyan-400"></div>

        <h2 className="mt-6 text-2xl font-bold text-white">
          Loading ...
        </h2>

        <p className="mt-2 text-slate-300">
          Fetching Lakehouse metrics...
        </p>

      </div>
    </div>
  );
}