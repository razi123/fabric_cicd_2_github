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

df = spark.sql("SELECT * FROM Lakehouse_Bronze.People_table LIMIT 1000")
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
