export const tableDetails = {
  sales_orders: {
    tableName: "sales_orders",
    formatVersion: "2",
    partitionSpec: "order_date",
    snapshots: 42,
    manifestFiles: 8,
    dataFiles: 324,
    storage: "18.4 GB",
    compression: "Parquet",
    optimized: "2 hours ago",
  },

  customer_dim: {
    tableName: "customer_dim",
    formatVersion: "2",
    partitionSpec: "customer_id",
    snapshots: 17,
    manifestFiles: 5,
    dataFiles: 87,
    storage: "5.2 GB",
    compression: "Parquet",
    optimized: "Yesterday",
  },

  inventory: {
    tableName: "inventory",
    formatVersion: "2",
    partitionSpec: "warehouse",
    snapshots: 66,
    manifestFiles: 15,
    dataFiles: 612,
    storage: "38.1 GB",
    compression: "Parquet",
    optimized: "3 days ago",
  },
};