export type TableName =
  | "orders"
  | "order_items"
  | "customers"
  | "products"
  | "stores"
  | "dim_date";

export interface IcebergTableData {
  id: number;
  table: TableName;
  namespace: string;
  files: number;
  size: string;
  status: "Healthy" | "Warning" | "Critical";
}