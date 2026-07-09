export default function SimulationHeader() {
  return (
    <div>

      <h1 className="text-4xl font-bold text-white">
        OCC Conflict Simulation
      </h1>

      <p className="mt-3 max-w-4xl text-slate-400 leading-7">
        This simulation demonstrates how Apache Iceberg uses
        <span className="font-semibold text-white">
          {" "}Optimistic Concurrency Control (OCC)
        </span>{" "}
        to prevent data corruption when multiple Spark sessions
        attempt to update the same table at the same time.
      </p>

    </div>
  );
}