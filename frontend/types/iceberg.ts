export type TableName =
  | "sales_orders"
  | "customer_dim"
  | "inventory";

export interface IcebergTableData {
  id: number;
  table: TableName;
  namespace: string;
  files: number;
  size: string;
  status: "Healthy" | "Warning" | "Critical";
}