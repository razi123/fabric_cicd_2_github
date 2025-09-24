# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d8a41520-fbd2-4395-8bba-4b99b9a05dcc",
# META       "default_lakehouse_name": "Lakehouse_Bronze",
# META       "default_lakehouse_workspace_id": "664afdb0-9225-479c-8c53-a7a229002c5f",
# META       "known_lakehouses": [
# META         {
# META           "id": "d8a41520-fbd2-4395-8bba-4b99b9a05dcc"
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

file_path = "Files/people-100.csv"
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


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
