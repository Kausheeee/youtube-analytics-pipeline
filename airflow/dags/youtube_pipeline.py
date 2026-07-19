from datetime import datetime, timezone
from pathlib import Path
from datetime import timedelta
from airflow.utils.email import send_email
import subprocess


from airflow.decorators import dag, task

PROJECT_ROOT = Path("/home/da-004/youtube-pipeline")
DBT_PROJECT = PROJECT_ROOT / "youtube_analytics"
DBT_EXECUTABLE = PROJECT_ROOT / "yt-venv" / "bin" / "dbt"

PYTHON_EXECUTABLE = PROJECT_ROOT / "yt-venv" / "bin" / "python"

def failure_notification(context):
    ti = context["task_instance"]
    dag_run = context["dag_run"]
    exception = context.get("exception")

    subject = f"❌ YouTube Pipeline Failed - {ti.task_id}"

    html_content = f"""
    <h2 style="color:red;">Pipeline Failed</h2>

    <table border="1" cellpadding="8">
        <tr><td><b>DAG</b></td><td>{ti.dag_id}</td></tr>
        <tr><td><b>Task</b></td><td>{ti.task_id}</td></tr>
        <tr><td><b>Run ID</b></td><td>{dag_run.run_id}</td></tr>
        <tr><td><b>Execution Date</b></td><td>{context['logical_date']}</td></tr>
        <tr><td><b>Host</b></td><td>{ti.hostname}</td></tr>
    </table>

    <h3>Exception</h3>

    <pre>{exception}</pre>

    <br>

    <a href="{ti.log_url}">
        View Airflow Logs
    </a>
    """

    send_email(
        to=["bendalamkaushik2002@gmail.com"],
        subject=subject,
        html_content=html_content,
    )

default_args = {
    "owner": "Kaushik",
    "email_on_failure": False,   # Disable default email
    "on_failure_callback": failure_notification,
}


@dag(
    dag_id="youtube_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="0 6 * * *",   # Every day at 6:00 AM
    catchup=False,
    tags=["youtube"],
    default_args=default_args,
)

def youtube_pipeline():

    @task
    def generate_snapshot_date():

        snapshot = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"Snapshot Date: {snapshot}")

        return snapshot

    @task
    def extract_data(snapshot_date):

        subprocess.run(
            [
                str(PYTHON_EXECUTABLE),
                str(PROJECT_ROOT / "extract.py"),
                "--snapshot-date",
                snapshot_date,
            ],
            cwd=str(PROJECT_ROOT),
            check=True,
        )

    @task
    def load_data(snapshot_date):

        subprocess.run(
            [
                str(PYTHON_EXECUTABLE),
                str(PROJECT_ROOT / "load.py"),
                "--snapshot-date",
                snapshot_date,
            ],
            cwd=str(PROJECT_ROOT),
            check=True,
        )

    @task
    def dbt_run():

        subprocess.run(
            [
                str(DBT_EXECUTABLE),
                "run",
                "--select",
                "marts",
            ],
            cwd=str(DBT_PROJECT),
            check=True,
        )

    @task
    def dbt_test():

        subprocess.run(
            [
                str(DBT_EXECUTABLE),
                "test",
            ],
            cwd=str(DBT_PROJECT),
            check=True,
        )

    # -----------------------------
    # Create task instances
    # -----------------------------

    snapshot = generate_snapshot_date()

    extract_task = extract_data(snapshot)

    load_task = load_data(snapshot)

    dbt_run_task = dbt_run()

    dbt_test_task = dbt_test()

    # -----------------------------
    # Define dependencies
    # -----------------------------

    extract_task >> load_task >> dbt_run_task >> dbt_test_task


youtube_pipeline()