
from airflow import DAG
from datetime import datetime

from inmobi_airflow_plugins.operators.kubernetes_create_resource import KubernetesCreateResourceFromFileOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

default_args = {
    'owner': 'central-platform',
    'start_date': datetime(2024, 2, 7),
}

dag = DAG('python-packages-runtime', default_args=default_args, schedule_interval=None)

create_k8s_resources = KubernetesCreateResourceFromFileOperator(
    task_id='create_k8s_resources',
    kubernetes_conn_id='key-vault-conn',
    yaml_conf="k8s_resources.yaml",
    dag=dag
)

# create_k8s_resources = KubernetesCreateResourceFromFileOperator(
#     task_id='create_k8s_resources',
#     kubernetes_conn_id='key-vault-conn',
#     yaml_conf="apiVersion: v1\nkind: Namespace\nmetadata:\n  name: test-namespace\n---\napiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: hello-world-dependencies-config-map\n  namespace: test-namespace\ndata:\n  requirements.txt: |\n    pandas==2.2.0",
#     dag=dag)

spark_task_on_k8s = SparkKubernetesOperator(
    task_id='spark_task_on_k8s',
    application_file='spark_application.yaml',
    kubernetes_conn_id="key-vault-conn",
    namespace="spark-application",
    watch=True,
    dag=dag
)

create_k8s_resources >> spark_task_on_k8s
