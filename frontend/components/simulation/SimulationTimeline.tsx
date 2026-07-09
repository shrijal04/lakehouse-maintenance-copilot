interface SimulationResponse {
  status: string;
  conflict: boolean;
  message: string;
  logs: string[];
  sessionA: string;
  sessionB: string;
}

interface Props {
  loading: boolean;
  result: SimulationResponse | null;
}

export default function SimulationTimeline({
  loading,
  result,
}: Props) {

  const sessionAStatus = loading
    ? "Running"
    : result?.sessionA ?? "Pending";

  const sessionBStatus = loading
    ? "Running"
    : result?.sessionB ?? "Pending";

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <h2 className="text-2xl font-semibold text-white">
        OCC Timeline
      </h2>

      <p className="mt-2 text-slate-400">
        This shows how both Spark sessions interact with the same Iceberg table.
      </p>

      <div className="mt-10 grid gap-12 lg:grid-cols-2">

        {/* SESSION A */}

        <div>

          <h3 className="mb-8 text-lg font-semibold text-white">
            Session A
          </h3>

          <TimelineItem
            title="Read Snapshot"
            description="Reads the current Iceberg snapshot."
            color="green"
          />

          <TimelineLine />

          <TimelineItem
            title="Sleep (20 seconds)"
            description="Waits before committing changes."
            color="yellow"
          />

          <TimelineLine />

          <TimelineItem
            title={
              sessionAStatus === "Committed"
                ? "Commit Successful"
                : sessionAStatus === "Failed"
                ? "Commit Failed (Conflict)"
                : sessionAStatus === "Running"
                ? "Waiting..."
                : "Pending"
            }
            description={
              sessionAStatus === "Committed"
                ? "Changes were successfully committed."
                : sessionAStatus === "Failed"
                ? "Iceberg rejected the outdated snapshot."
                : "Waiting for commit."
            }
            color={
              sessionAStatus === "Committed"
                ? "green"
                : sessionAStatus === "Failed"
                ? "red"
                : sessionAStatus === "Running"
                ? "blue"
                : "gray"
            }
          />

        </div>

        {/* SESSION B */}

        <div>

          <h3 className="mb-8 text-lg font-semibold text-white">
            Session B
          </h3>

          <TimelineItem
            title="Read Snapshot"
            description="Reads the same snapshot as Session A."
            color="green"
          />

          <TimelineLine />

          <TimelineItem
            title="Update Row"
            description="Immediately updates Order ID 1."
            color="yellow"
          />

          <TimelineLine />

          <TimelineItem
            title={
              sessionBStatus === "Committed"
                ? "Commit Successful"
                : sessionBStatus === "Failed"
                ? "Commit Failed"
                : sessionBStatus === "Running"
                ? "Waiting..."
                : "Pending"
            }
            description={
              sessionBStatus === "Committed"
                ? "Successfully created a new snapshot."
                : sessionBStatus === "Failed"
                ? "Commit failed."
                : "Waiting for commit."
            }
            color={
              sessionBStatus === "Committed"
                ? "green"
                : sessionBStatus === "Failed"
                ? "red"
                : sessionBStatus === "Running"
                ? "blue"
                : "gray"
            }
          />

        </div>

      </div>

      {result?.conflict && (

        <div className="mt-10 rounded-xl border border-red-500/30 bg-red-500/10 p-5">

          <h3 className="text-lg font-semibold text-red-400">
            Why did the conflict happen?
          </h3>

          <p className="mt-3 leading-7 text-slate-300">
            Both Spark sessions started from the same Iceberg snapshot.
            Session B finished first and created a newer snapshot.
            When Session A tried to commit, it was still using the old
            snapshot. Apache Iceberg detected that the table had already
            changed and rejected Session A's transaction to prevent data
            corruption.
          </p>

        </div>

      )}

    </div>
  );
}

function TimelineItem({
  title,
  description,
  color,
}: {
  title: string;
  description: string;
  color: "green" | "yellow" | "red" | "blue" | "gray";
}) {

  const colors = {
    green: "bg-green-500",
    yellow: "bg-yellow-400",
    red: "bg-red-500",
    blue: "bg-blue-500",
    gray: "bg-slate-500",
  };

  return (
    <div className="flex gap-4">

      <div className={`mt-1 h-5 w-5 rounded-full ${colors[color]}`} />

      <div>

        <h4 className="font-semibold text-white">
          {title}
        </h4>

        <p className="mt-1 text-sm leading-6 text-slate-400">
          {description}
        </p>

      </div>

    </div>
  );
}

function TimelineLine() {
  return (
    <div className="ml-2 h-8 w-0.5 bg-slate-700" />
  );
}