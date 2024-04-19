import os
from datetime import datetime

import yaml
from airflow import DAG
from airflow.operators.python import PythonOperator
from inmobi_airflow_plugins.operators.kubernetes_create_resource import KubernetesCreateResourceFromFileOperator
# from airflow.providers.cncf.kubernetes.operators.resource import KubernetesCreateResourceOperator


default_args = {
    'owner': 'central-platform',
    'start_date': datetime(2024, 1, 8),
}

dag = DAG('yaml-parser', default_args=default_args, schedule_interval=None)
createResource = KubernetesCreateResourceFromFileOperator(
    task_id='createResource',
    kubernetes_conn_id='key-vault-conn',
    yaml_conf="multiple_documents.yaml",
    dag=dag)

# createResource = KubernetesCreateResourceFromFileOperator(
#     task_id='createResource',
#     kubernetes_conn_id='key-vault-conn',
#     yaml_conf="apiVersion: v1\nkind: Namespace\nmetadata:\n  name: {{ var.value.testNamespace }}\n---\napiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: hello-world-dependencies-config-map\n  namespace: {{ var.value.testNamespace }}\ndata:\n  requirements.txt: |\n    pandas==2.2.0",
#     dag=dag)

# yaml_file_path = "/opt/airflow/git/airflow-spark-on-k8s.git/dags/python/multiple_documents.yaml"

# def load_yaml_file_with_multiple_documents():
#     with open(os.path.abspath(yaml_file_path)) as f:
#         try:
#             yaml_objects = yaml.safe_load_all(f)
#             print(yaml_objects)
#         except yaml.YAMLError as exc:
#             print(exc)
#             raise ValueError(f"Error loading YAML from {yaml_file_path}")

# def read_yaml_task():
#     print("Running end_task")
