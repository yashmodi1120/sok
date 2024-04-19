from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 3
}

dag = DAG(
    'spark_pi',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    tags=['example']
)


submit = SparkKubernetesOperator(
    task_id='spark_pi_submit',
    namespace="spark-test",
    application_file="example_spark_kubernetes_operator_pi.yaml",
    kubernetes_conn_id="kubernetes_in_cluster",
    dag=dag,
)

submit
