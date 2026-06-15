from __future__ import annotations
from airflow.sdk import dag, task
#from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd
import pendulum
import sys
import os
import time


from airflow.providers.standard.operators.python import PythonOperator

import pathlib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))
from gather_tracks import fetch_list_of_file, gather_all_top_tracks, write_gather_top_tracks

# [START dag_decorator_usage]

@dag(

    schedule=None,

    start_date=pendulum.today("Europe/Paris"),
    
    catchup=False,

    tags=["test"],

    dag_display_name="gather_top_tracks_spotify",

)

def gather_top_tracks_spotify():
    """
    Decorator pour dag d'import du Billboard
    """
    print("Fetching starts here")
    print(os.getcwd())
    @task()    
    def fetch_top_tracks(retries = 3):
        print("Fetching starts here")
        print(pathlib.Path(__file__).parent.resolve())
        return fetch_list_of_file()
    @task()    
    def transform_top_tracks(list_of_file,retries = 3):
        print("Transforming starts here")
        gather_all_top_tracks(list_of_file)
    @task()    
    def write_top_tracks(retries = 3):
        print("Writing starts here")
        write_gather_top_tracks()
    
    @task()    
    def display_Task2(retries = 3):
        print("Second Task")

    display_Task2()
    list_of_file = fetch_top_tracks()
    transform_top_tracks(list_of_file)
    write_top_tracks()

gather_top_tracks_spotify()

# [END dag_decorator_usage]


