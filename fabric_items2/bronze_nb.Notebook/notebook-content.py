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
# META     },
# META     "environment": {
# META       "environmentId": "ff86fa34-8a49-9c11-4b67-87dd3c3357ec",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
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

from fabric_utils.transform_utils import clean_column_names, mask_email  #, add_age, add_year_column

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

if __name__ == "__main__":
    file_path = "Files/people-100.csv"
    # file_path = source_path
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(file_path)

    df_transformed = (
        df.transform(clean_column_names)
          .transform(mask_email)
        #   .transform(add_age)
        #   .transform(add_year_column)
    )

    display(df_transformed)

    df_transformed.write.format("delta") \
        .mode("overwrite") \
        .saveAsTable("Lakehouse_Bronze.People_table")

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
