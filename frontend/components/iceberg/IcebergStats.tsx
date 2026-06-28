import IcebergMetricCard from "./IcebergMetricCard";

import { icebergMetrics } from "@/data/iceberg";

export default function IcebergStats() {
  return (
    <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">
      {icebergMetrics.map((metric) => (
        <IcebergMetricCard
          key={metric.id}
          title={metric.title}
          value={metric.value}
          description={metric.description}
          icon={metric.icon}
        />
      ))}
    </div>
  );
}