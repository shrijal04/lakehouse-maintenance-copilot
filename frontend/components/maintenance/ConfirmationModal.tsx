"use client";

interface Props {
  open: boolean;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function ConfirmationModal({
  open,
  message,
  onConfirm,
  onCancel,
}: Props) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">

      <div className="w-[500px] rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-2xl">

        <h2 className="text-2xl font-bold text-white">
          Confirm Maintenance
        </h2>

        <p className="mt-5 whitespace-pre-line text-slate-300">
          {message}
        </p>

        <div className="mt-8 flex justify-end gap-4">

          <button
            onClick={onCancel}
            className="rounded-xl border border-slate-600 px-5 py-2 text-white hover:bg-slate-800"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className="rounded-xl bg-cyan-600 px-5 py-2 text-white hover:bg-cyan-500"
          >
            Confirm
          </button>

        </div>

      </div>

    </div>
  );
}