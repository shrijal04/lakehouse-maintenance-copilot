import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.manager import SparkManagerService

spark = SparkManagerService().get_spark()

# -------------------------------------------------------
# Create Bronze Namespace
# -------------------------------------------------------

# spark.sql("""
# CREATE NAMESPACE IF NOT EXISTS local.bronze
# """)

# print("✓ Bronze namespace created.")

# # -------------------------------------------------------
# # Create Silver Namespace
# # -------------------------------------------------------

# spark.sql("""
# CREATE NAMESPACE IF NOT EXISTS local.silver
# """)

# print("✓ Silver namespace created.")

# # -------------------------------------------------------
# # Create Gold Namespace
# # -------------------------------------------------------

# spark.sql("""
# CREATE NAMESPACE IF NOT EXISTS local.gold
# """)

# print("✓ Gold namespace created.")

# print("\nAll namespaces are ready!")

spark.sql("SHOW NAMESPACES IN local").show(truncate=False)