from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from app.repositories.chart_repository import ChartRepository


class ChartGenerator:

    def __init__(self):

        self.repo = ChartRepository()

        self.output = Path("reports/charts")
        self.output.mkdir(parents=True, exist_ok=True)

    def health_score_chart(self):

        data = self.repo.get_health_history()

        if not data:
            return

        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 5))

        for table in df["table_name"].unique():

            table_df = df[df["table_name"] == table]

            plt.plot(
                table_df["recorded_at"],
                table_df["health_score"],
                label=table,
            )

        plt.title("Health Score Trend")

        plt.xlabel("Time")

        plt.ylabel("Health Score")

        plt.legend()

        plt.tight_layout()

        plt.savefig(self.output / "health_score.png")

        plt.close()
    
    def snapshot_chart(self):

        data = self.repo.get_health_history()

        if not data:
            return

        df = pd.DataFrame(data)

        plt.figure(figsize=(10,5))

        for table in df["table_name"].unique():

            table_df = df[df["table_name"] == table]

            plt.plot(
                table_df["recorded_at"],
                table_df["snapshot_count"],
                label=table,
            )

        plt.title("Snapshot Count")

        plt.xlabel("Time")

        plt.ylabel("Snapshots")

        plt.legend()

        plt.tight_layout()

        plt.savefig(self.output / "snapshots.png")

        plt.close()

    def data_files_chart(self):

        data = self.repo.get_health_history()

        if not data:
            return

        df = pd.DataFrame(data)

        plt.figure(figsize=(10,5))

        for table in df["table_name"].unique():

            table_df = df[df["table_name"] == table]

            plt.plot(
                table_df["recorded_at"],
                table_df["data_file_count"],
                label=table,
            )

        plt.title("Data File Count")

        plt.xlabel("Time")

        plt.ylabel("Files")

        plt.legend()

        plt.tight_layout()

        plt.savefig(self.output / "data_files.png")

        plt.close()

    def average_file_chart(self):

        data = self.repo.get_health_history()

        if not data:
            return

        df = pd.DataFrame(data)

        plt.figure(figsize=(10,5))

        for table in df["table_name"].unique():

            table_df = df[df["table_name"] == table]

            plt.plot(
                table_df["recorded_at"],
                table_df["average_file_kb"],
                label=table,
            )

        plt.title("Average File Size")

        plt.xlabel("Time")

        plt.ylabel("KB")

        plt.legend()

        plt.tight_layout()

        plt.savefig(self.output / "average_file_size.png")

        plt.close()

    def storage_chart(self):

        data = self.repo.get_health_history()

        if not data:
            return

        df = pd.DataFrame(data)

        plt.figure(figsize=(10,5))

        for table in df["table_name"].unique():

            table_df = df[df["table_name"] == table]

            plt.plot(
                table_df["recorded_at"],
                table_df["total_size_mb"],
                label=table,
            )

        plt.title("Lakehouse Storage")

        plt.xlabel("Time")

        plt.ylabel("MB")

        plt.legend()

        plt.tight_layout()

        plt.savefig(self.output / "storage.png")

        plt.close()

    def generate_all(self):

        self.health_score_chart()

        self.snapshot_chart()

        self.data_files_chart()

        self.average_file_chart()

        self.storage_chart()