from airflow.operators.bash import BashOperator
from airflow import DAG
from airflow.models import Variable
from datetime import datetime

default_args = {
    'owner': 'central-platform',
    'start_date': datetime(2024, 1, 10)
}

# 'email_on_failure': True,
# 'email': 'ayush.raj@inmobi.com'

dag = DAG('bash_dag', default_args=default_args, schedule_interval=None)

bash_task = BashOperator(
    task_id="bash_task",
    bash_command="scripts/my_script.sh",
    # bash_command="ls /opt/airflow/git/airflow-spark-on-k8s.git/dags/testing",
    do_xcom_push=True,
    dag=dag
)

# bash_task = BashOperator(
#     task_id="bash_task",
#     # bash_command="cat /opt/airflow/dags/requirements.txt && echo '--------' && ls /opt/airflow/git/airflow-spark-on-k8s.git/plugins && echo 'list python packages' && pip list",
#     bash_command="pip list && echo '-------' && ls /opt/airflow/dags && echo '-------' && ls /opt/airflow/git/airflow-spark-on-k8s.git",
#     # bash_command="echo '{{ var.value.CamelCasingSecret }}'",
#     # env={"sample_variable": Variable.get("sample-variable")},
#     do_xcom_push=False,
#     dag=dag
# )

bash_task
