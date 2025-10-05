# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8008b2a1-fdf8-4b1a-b920-c1b31dc18f4f",
# META       "default_lakehouse_name": "Lakehouse_Bronze",
# META       "default_lakehouse_workspace_id": "5871c70b-6796-4e24-9444-9af3e4daa27c",
# META       "known_lakehouses": [
# META         {
# META           "id": "8008b2a1-fdf8-4b1a-b920-c1b31dc18f4f"
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
    # file_path = "Files/raw-data/people-100.csv"
    file_path = source_path
    print(f"source_path : {source_path}")
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

# 
print("I am in the old feature branch")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
