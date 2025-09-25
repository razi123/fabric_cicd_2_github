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
# META       "default_lakehouse_workspace_id": "24fbb753-b211-47f0-9acf-ad7e07029fc8",
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

# file_path = "Files/raw-data/people-100.csv"
# # Read CSV into Spark DataFrame
# df = spark.read.format("csv") \
#     .option("header", "true") \
#     .option("inferSchema", "true") \
#     .load(file_path)

# display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# lowercase, replace spaces with underscores
def clean_column_names(df):
    for col in df.columns:
        df = df.withColumnRenamed(col, col.strip().lower().replace(" ", "_"))
    return df


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Mask emails for privacy (show only first letter + domain)

def mask_email(df):
    return df.withColumn(
        "email_masked",
        F.concat(
            F.substring("email", 1, 1),
            F.lit("***@"),
            F.regexp_extract("email", "@(.+)", 1)
        )
    )


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************
# Calculate age from Date_of_birth
def add_age(df):
    return df.withColumn(
        "age",
        F.floor(F.datediff(F.current_date(), F.to_date("date_of_birth")) / 365)
    )

# METADATA ********************
# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
# CELL ********************

# -------------------------------
# Apply transformations
# -------------------------------
# df_transformed = (
#     df.transform(clean_column_names)
#       .transform(mask_email)
#       .transform(add_age)
# )

# display(df_transformed)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Example: write DataFrame into Lakehouse managed tables
# df_transformed.write.format("delta") \
#     .mode("overwrite") \
#     .saveAsTable("Lakehouse_Bronze.People_table")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ------------------ only runs in Fabric, not during tests ------------------
if __name__ == "__main__":
    file_path = "Files/raw-data/people-100.csv"

    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(file_path)

    df_transformed = (
        df.transform(clean_column_names)
          .transform(mask_email)
          .transform(add_age)
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
