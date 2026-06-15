#

from __future__ import annotations
from airflow.sdk import dag, task
#from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd
import pendulum
import sys
import os
#sys.path.append("../")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))
import pathlib

#os.chdir("../")

print(os.getcwd())
with os.scandir(".") as d:
    for e in d:
        print(e.name)

from spotify import fetch_data
#print(fetch_data)
#os.chdir('/home/kesav/airflow_project/lib')

#start_date=pendulum.today("Europe/Paris"), pendulum.datetime(2013, 3, 31, 2, 30, tz='Europe/Paris')
@dag(schedule=None,
     start_date= pendulum.datetime(2026, 1, 1, 0, 0, tz='Europe/Paris'),
     tags=[]

)

def fetch_data_from_spotify():
    """
    Decorator pour dag d'import
    """
    print("Fetching starts here 1")
    print(os.getcwd())
    @task()    
    def fetch(retries = 3):
        print("Fetching starts here")
        print(pathlib.Path(__file__).parent.resolve())
        fetch_data()
        print("")
    
    @task()    
    def display_Task(retries = 3):
        print("Second Task")

    display_Task()
    fetch()
fetch_data_from_spotify()

# [END dag_decorator_usage]





