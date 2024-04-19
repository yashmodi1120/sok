from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

def end_task():
    print("Running end_task")

default_args = {
    'owner': 'central-platform',
    'start_date': datetime(2024, 1, 10),
}

dag = DAG('branch_tasks_on_failure', default_args=default_args, schedule_interval=None)

start_task = DummyOperator(
    task_id='start_task',
    dag=dag
)

spark_task_on_k8s = SparkKubernetesOperator(
    task_id='spark_task_on_k8s',
    application_file='spark-hello-world.yaml',
    namespace="spark-application",
    kubernetes_conn_id="key-vault-conn",
    watch=True,
    dag=dag
)

new_cluster_conf = {
    'spark_version': '13.3.x-scala2.12',
    'node_type_id': 'Standard_DS3_v2',
    "autoscale": {
        "min_workers": 1,
        "max_workers": 2
    }
}

spark_task_on_databricks = DatabricksSubmitRunOperator(
    task_id='spark_task_on_databricks',
    trigger_rule='all_failed',
    dag=dag,
    new_cluster=new_cluster_conf,
    databricks_conn_id='databricks_mlp_connection',
    spark_submit_task={'parameters': ["--class", "org.apache.spark.examples.SparkPi", "dbfs:/FileStore/amit/spark_examples_2_12_3_4_1.jar", "10"]},
)

follow_up_task = DummyOperator(
    task_id='follow_up_task',
    dag=dag,
    trigger_rule='none_failed'
)

end_task = PythonOperator(
    task_id='end_task',
    python_callable=end_task,
    dag=dag
)

start_task >> spark_task_on_k8s >> spark_task_on_databricks >> follow_up_task >> end_task
