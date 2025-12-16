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

from lib.spotify import main

import pendulum


from airflow.providers.standard.operators.python import PythonOperator

from airflow.sdk import dag, task



# [START dag_decorator_usage]

@dag(

    schedule=None,

    start_date=pendulum.datetime(2025, 11, 15, tz="UTC+1"),

    catchup=False,

    tags=["test"],

    dag_display_name="Spotify",

)

def fetch_data_from_spotify():

    sample_task_1 = PythonOperator(

        task_id="main"

    )


    @task(task_display_name="Sample Task 2")

    def sample_task_2():

        pass


    sample_task_1()



fetch_data_from_spotify()

# [END dag_decorator_usage]











