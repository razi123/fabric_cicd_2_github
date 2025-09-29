from pyspark.sql import functions as F

def clean_column_names(df):
    for col in df.columns:
        df = df.withColumnRenamed(col, col.strip().lower().replace(" ", "_"))
    return df

def mask_email(df):
    return df.withColumn(
        "email_masked",
        F.concat(
            F.substring("email", 1, 1),
            F.lit("***@"),
            F.regexp_extract("email", "@(.+)", 1)
        )
    )

# def add_age(df):
#     return df.withColumn(
#         "age",
#         F.floor(F.datediff(F.current_date(), F.to_date("date_of_birth")) / 365)
#     )

# def add_year_column(df):
#     return df.withColumn("year", F.year(F.col("date_of_birth")))
