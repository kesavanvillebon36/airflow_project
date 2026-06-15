#

# Licensed to the Apache Software Foundation (ASF) under one

# or more contributor license agreements.  See the NOTICE file

# distributed with this work for additional information

# regarding copyright ownership.  The ASF licenses this file

# to you under the Apache License, Version 2.0 (the

# "License"); you may not use this file except in compliance

# with the License.  You may obtain a copy of the License at

#

#   http://www.apache.org/licenses/LICENSE-2.0

#

# Unless required by applicable law or agreed to in writing,

# software distributed under the License is distributed on an

# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY

# KIND, either express or implied.  See the License for the

# specific language governing permissions and limitations

# under the License.

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
from billboard import fetch_data_billboard, transform_data_billboard, write_table_billboard

# [START dag_decorator_usage]

@dag(

    schedule=None,

    start_date=pendulum.today("Europe/Paris"),
    
    catchup=False,

    tags=["test"],

    dag_display_name="fetch_transform_data_from_billboard",

)

def fetch_transform_data_from_billboard():
    """
    Decorator pour dag d'import du Billboard
    """
    print("Fetching starts here 1")
    print(os.getcwd())
    @task()    
    def fetch_billboard(retries = 3):
        print("Fetching starts here")
        print(pathlib.Path(__file__).parent.resolve())
        fetch_data_billboard()
    @task()    
    def transform_billboard(retries = 3):
        print("Transforming starts here")
        transform_data_billboard()
    @task()    
    def write_billboard(retries = 3):
        print("Transforming starts here")
        write_table_billboard()
    
    @task()    
    def display_Task2(retries = 3):
        print("Second Task")

    display_Task2()
    fetch_billboard()
    transform_billboard()
    write_billboard()

fetch_transform_data_from_billboard()

# [END dag_decorator_usage]
