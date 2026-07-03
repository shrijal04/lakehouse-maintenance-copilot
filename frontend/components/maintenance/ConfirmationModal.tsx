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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">

      <div
        className="
          flex
          max-h-[90vh]
          w-full
          max-w-2xl
          flex-col
          overflow-hidden
          rounded-2xl
          border
          border-slate-700
          bg-slate-900
          shadow-2xl
        "
      >
        {/* Header */}

        <div className="border-b border-slate-700 px-6 py-5">
          <h2 className="text-2xl font-bold text-white">
            Confirm Maintenance
          </h2>
        </div>

        {/* Body */}

        <div className="flex-1 overflow-y-auto px-6 py-5">
          <p className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-300">
            {message}
          </p>
        </div>

        {/* Footer */}

        <div className="flex justify-end gap-3 border-t border-slate-700 px-6 py-4">

          <button
            onClick={onCancel}
            className="rounded-xl border border-slate-600 px-5 py-2 text-white transition hover:bg-slate-800"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className="rounded-xl bg-cyan-600 px-5 py-2 text-white transition hover:bg-cyan-500"
          >
            Confirm
          </button>

        </div>
      </div>

    </div>
  );
}