import findspark
findspark.init()

import pytest
import os
import sys 
import importlib.util
from pyspark.sql import SparkSession

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "fabric_items2", "bronze_nb.Notebook", "notebook-content.py")

spec = importlib.util.spec_from_file_location("bronze_nb", NOTEBOOK_PATH)
bronze_nb = importlib.util.module_from_spec(spec)
sys.modules["bronze_nb"] = bronze_nb
spec.loader.exec_module(bronze_nb)

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-pyspark") \
        .getOrCreate()
    yield spark
    spark.stop()


## tests below
def test_clean_column_names(spark):
    data = [(1, "Alice")]
    df = spark.createDataFrame(data, ["Id ", " Full Name "])
    df_clean = bronze_nb.clean_column_names(df)
    assert set(df_clean.columns) == {"id", "full_name"}

def test_mask_email(spark):
    data = [(1, "alice.smith@example.com")]
    df = spark.createDataFrame(data, ["id", "email"])
    df_masked = bronze_nb.mask_email(df)
    result = df_masked.select("email_masked").collect()[0][0]
    assert result.startswith("a***@")
    assert result.endswith("example.com")

def test_add_age(spark):
    data = [(1, "1990-01-01")]
    df = spark.createDataFrame(data, ["id", "date_of_birth"])
    df_age = bronze_nb.add_age(df)
    age = df_age.select("age").collect()[0][0]
    assert isinstance(age, int)
    assert age > 30

# def test_add_year_column(spark):
#     data = [(1, "1990-01-01")]
#     df = spark.createDataFrame(data, ["id", "Date_of_birth"])
#     df_year = bronze_nb.add_year_column(df)
#     year = df_year.select("year").collect()[0][0]
#     assert year == 1990