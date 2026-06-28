import { IcebergTableData } from "@/types/iceberg";

export const icebergTables: IcebergTableData[] = [
  {
    id: 1,
    table: "sales_orders",
    namespace: "sales",
    files: 324,
    size: "18.4 GB",
    status: "Healthy",
  },
  {
    id: 2,
    table: "customer_dim",
    namespace: "analytics",
    files: 87,
    size: "5.2 GB",
    status: "Warning",
  },
  {
    id: 3,
    table: "inventory",
    namespace: "warehouse",
    files: 612,
    size: "38.1 GB",
    status: "Critical",
  },
];