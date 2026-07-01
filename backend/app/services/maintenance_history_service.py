from sqlalchemy import text

from app.database import engine


class MaintenanceHistoryRepository:

    def __init__(self):
        self.engine = engine

    def save_maintenance_job(self, job):

        with self.engine.begin() as conn:

            conn.execute(
                text("""
                    INSERT INTO maintenance_history
                    (
                        table_name,
                        status,
                        duration_seconds,

                        files_rewritten,
                        files_added,
                        bytes_rewritten,

                        manifests_rewritten,
                        manifests_added,

                        snapshots_deleted,
                        manifest_files_deleted,
                        manifest_lists_deleted,

                        orphan_files_removed
                    )

                    VALUES
                    (
                        :table_name,
                        :status,
                        :duration_seconds,

                        :files_rewritten,
                        :files_added,
                        :bytes_rewritten,

                        :manifests_rewritten,
                        :manifests_added,

                        :snapshots_deleted,
                        :manifest_files_deleted,
                        :manifest_lists_deleted,

                        :orphan_files_removed
                    )
                """),
                job,
            )

    def get_maintenance_history(
        self,
        table_name: str,
    ):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        finished_at,
                        status,
                        duration_seconds,
                        files_rewritten,
                        manifests_rewritten,
                        snapshots_deleted,
                        orphan_files_removed
                    FROM maintenance_history
                    WHERE table_name = :table_name
                    ORDER BY finished_at ASC
                """),
                {
                    "table_name": table_name,
                },
            )

            return [
                {
                    "finished_at": row.finished_at,
                    "status": row.status,
                    "duration_seconds": row.duration_seconds,
                    "files_rewritten": row.files_rewritten,
                    "manifests_rewritten": row.manifests_rewritten,
                    "snapshots_deleted": row.snapshots_deleted,
                    "orphan_files_removed": row.orphan_files_removed,
                }
                for row in result
            ]