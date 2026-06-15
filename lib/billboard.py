import requests
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from airflow.sdk import Connection, Variable

def fetch_data_billboard():
    data_billboard = pd.read_json("https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json")
    data_billboard.to_json("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT_raw.json")
    



def transform_data_billboard():
    # Expand the "data" column into rows
    
    new = pd.read_json("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT_raw.json")
    exploded = new.explode("data", ignore_index=True)

    # Normalize each dict inside "data"
    normalized = pd.json_normalize(exploded["data"])

    # Add the date column back (automatically aligned after explode)
    normalized["date"] = exploded["date"]

    # Reorder columns
    normalized[["date"] + [col for col in normalized.columns if col != "date"]].to_json("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT_transformed.json")


def write_table_billboard():
    transformed_dataset = pd.read_json("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT_transformed.json")
    table = pa.Table.from_pandas(transformed_dataset)
    pq.write_table(table, "/home/kesav/airflow_project/raw/billboard/billboard_100_OAT.parquet")
    transformed_dataset.to_json("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT.json")
    transformed_dataset.to_csv("/home/kesav/airflow_project/raw/billboard/billboard_100_OAT.csv", index=False)


def fetch_billboard_data():
    fetch_data_billboard()
    transform_data_billboard()
    write_table_billboard()


if __name__ == "__main__":
    fetch_billboard_data()


postgres_username = Variable.get("postgres_username")
postgres_password =  Variable.get("postgres_password")


def connect_base():
    c = Connection(
        conn_id="some_conn",
        conn_type="postgres",
        description="connection description",
        host="localhost",
        login=postgres_username,
        password=postgres_password,
        extra={"this_param": "some val", "that_param": "other val*"},
    )
    print(f"AIRFLOW_CONN_{c.conn_id.upper()}='{c.as_json()}'")
    AIRFLOW_CONN_SOME_CONN='{"conn_type": "mysql", "description": "connection description", "host": "myhost.com", "login": "myname", "password": "mypassword", "extra": {"this_param": "some val", "that_param": "other val*"}}'
    print(AIRFLOW_CONN_SOME_CONN)


