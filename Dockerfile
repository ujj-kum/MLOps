# slim-buster is a lightweight version of the Debian OS having python 3.8 installed
# This image will be used to run the python scripts
FROM python:3.8-slim-buster
USER root
RUN mkdir /app
# Copies everything in the current directory(.dockerignore files excluded) 
# to /app in the container
COPY . /app
# Setting/app/ as the working directory for any subsequent commands in the Dockerfile
WORKDIR /app/
RUN pip install -r requirements.txt
# Sets an environment variable 
# Make sure to have no spaces around the equal sign
# In local, we have airflow folder, that will be copied to the container
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True
RUN airflow db init
# -e flag is used to create a user with the email address provided
RUN airflow users create --email batman.c731@gmail.com \
                         --firstname Bruce \
                         --lastname Wayne \
                         --password admin \
                         --role Admin \
                         --username admin
# 7 → Read (r) + Write (w) + Execute (x) for Owner.(111)
# 7 → Read (r) + Write (w) + Execute (x) for Group.
# 7 → Read (r) + Write (w) + Execute (x) for Others
RUN chmod 777 start.sh
RUN apt update -y
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]