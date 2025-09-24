# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e835c292-d746-4878-9dca-8758d7d3a7cf",
# META       "default_lakehouse_name": "Lakehouse_Bronze",
# META       "default_lakehouse_workspace_id": "c995b3b9-434b-4255-9848-874d1d26ff3e",
# META       "known_lakehouses": [
# META         {
# META           "id": "e835c292-d746-4878-9dca-8758d7d3a7cf"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Full Lakehouse ABFSS path
# file_path = "abfss://DEWorkshop_raziuddinkhazi_dev@onelake.dfs.fabric.microsoft.com/Lakehouse_Bronze.Lakehouse/Files/people-100.csv"
# file_path = "abfss://DEWorkshop_raziuddinkhazi_feature@onelake.dfs.fabric.microsoft.com/Lakehouse_Bronze.Lakehouse/Files/people-100.csv"

file_path = "Files/raw-data/people-100.csv"
# Read CSV into Spark DataFrame
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(file_path)

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Example: write DataFrame into Lakehouse managed tables
df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("Lakehouse_Bronze.People_table")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

