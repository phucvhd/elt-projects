# Use the official Airflow image as the base
FROM apache/airflow:latest
# Install the Docker provider for Airflow
RUN pip install apache-airflow-providers-docker apache-airflow-providers-standard
RUN pip install apache-airflow-providers-fab
WORKDIR /opt/airflow