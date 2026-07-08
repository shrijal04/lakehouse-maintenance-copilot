class HealthScoreService:
    """
    Calculates the health score of a table.

    Final score ranges from 0 to 100.
    """

    @staticmethod
    def calculate(metrics: dict) -> int:

        score = 100

        # -----------------------------
        # Snapshot Count
        # -----------------------------
        if metrics["snapshot_count"] > 100:
            score -= 30
        elif metrics["snapshot_count"] > 40:
            score -= 15

        # -----------------------------
        # Average File Size
        # -----------------------------
        if metrics["average_file_kb"] < 64:
            score -= 30
        elif metrics["average_file_kb"] < 128:
            score -= 15

        # -----------------------------
        # Data Files
        # -----------------------------
        if metrics["data_file_count"] > 40:
            score -= 20

        # -----------------------------
        # Manifest Files
        # -----------------------------
        if metrics["manifest_file_count"] > 100:
            score -= 10

        # -----------------------------
        # Orphan Files
        # -----------------------------
        if metrics["orphan_file_count"] > 0:
            score -= 10

        return max(score, 0)