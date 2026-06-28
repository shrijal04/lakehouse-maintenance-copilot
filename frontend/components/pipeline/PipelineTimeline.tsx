import { timelineEvents } from "@/data/pipeline";

export default function PipelineTimeline() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Pipeline Timeline
      </h2>

      <div className="space-y-6">
        {timelineEvents.map((event) => (
          <div
            key={event.time}
            className="flex items-start gap-4"
          >
            <div className="mt-2 h-3 w-3 rounded-full bg-cyan-400" />

            <div>
              <p className="text-sm text-slate-400">
                {event.time}
              </p>

              <h3 className="font-semibold text-white">
                {event.title}
              </h3>

              <span className="text-cyan-400 text-sm">
                {event.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}