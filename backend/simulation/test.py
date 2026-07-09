import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from simulation.spark_factory import create_spark

spark1 = create_spark("SessionA")
spark2 = create_spark("SessionB")

print(id(spark1))
print(id(spark2))
print(spark1 is spark2)