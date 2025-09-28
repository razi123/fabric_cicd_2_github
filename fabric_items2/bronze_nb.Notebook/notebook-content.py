# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
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

def add_year_column(df):
    return df.withColumn("year", F.year(F.col("Date_of_birth")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

if __name__ == "__main__":
    # file_path = "Files/people-100.csv"
    file_path = source_path
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(file_path)

    df_transformed = (
        df.transform(clean_column_names)
          .transform(mask_email)
          .transform(add_age)
          .transform(add_year_column)
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
