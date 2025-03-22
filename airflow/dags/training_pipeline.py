from __future__ import annotations
import numpy as np
import json
import os
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.pipeline.train_pipeline import TrainingPipeline

training_pipeline = TrainingPipeline()

with DAG(
    dag_id="gemstone_training_pipeline",
    default_args={"retries":2},
    description="A training pipeline for gemstone prediction",
    schedule=@weekly,
    start_date=pendulum.datetime(2025, 3, 21, tz="UTC"),
    catchup=False,
    tags=["training"],
) as dag:

    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        # ti -> task instance
        ti = kwargs["ti"]
        train_data_path, test_data = training_pipeline.start_data_ingestion()
        ti.xcom_push('data_ingestion_artifact', {
            "train_data_path": train_data_path, 
            "test_data_path": test_data_path}
        )

    def data_transformation(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion_artifact",
                                               key="data_ingestion_artifact", 
                                              )
        train_arr, test_arr = training_pipeline.start_data_transformation(data_ingestion_artifact)
        train_arr = train_arr.to_list()
        test_arr = test_arr.to_list()
        ti.xcom_push('data_transformation_artifact', {
            "train_arr": train_arr, 
            "test_arr": test_arr}
        )

    def model_trainer(**kwargs):
        ti = kwargs["ti"]
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation_artifact",
                                               key="data_transformation_artifact", 
                                              )
        train_arr = np.array(object=data_transformation_artifact["train_arr"])
        test_arr = np.array(object=data_transformation_artifact["test_arr"])
        training_pipeline.start_model_training(train_arr, test_arr)

    def push_data_to_s3(**kwargs):
        bucket_name = os.getenv(key="BUCKET_NAME")
        artifact_path = "/app/artifacts"
        os.system(f"aws s3 cp {artifact_path} s3://{bucket_name}/artifacts")

    # Python Operators
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        """\
        #### Task Documentation
        This task is responsible for ingesting the data from the source.
        """
    )

    data_transform_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformation,
    )
    data_transform_task.doc_md = dedent(
        """\
        #### Task Documentation
        This task is responsible for transforming the data.
        """
    )


    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """\
        #### Task Documentation
        This task is responsible for training the model.
        """
    )


    push_data_to_s3 = PythonOperator(
        task_id="push_data_to_s3",
        python_callable=push_data_to_s3,
    )


data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_to_s3