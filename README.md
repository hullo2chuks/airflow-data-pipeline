# Data Pipelines with Airflow

This project involves creating custom operators to execute essential functions like staging data, populating a data warehouse, and validating data through the pipeline.

A helper class containing all necessary SQL transformations is at your disposal. While you won't have to write the ETL processes, your responsibility lies in executing them using your custom operators.

## Initiating the Airflow Web Server
Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed before proceeding.

To bring up the entire app stack up, we use [docker-compose](https://docs.docker.com/engine/reference/commandline/compose_up/) as shown below

```bash
docker-compose up -d
```
Visit http://localhost:8080 once all containers are up and running.

## Configuring Connections in the Airflow Web Server UI
![Airflow Web Server UI. Credentials: `airflow`/`airflow`.](assets/login.png)

On the Airflow web server UI, use `airflow` for both username and password.
* Post-login, navigate to **Admin > Connections** to add required connections - specifically, `aws_credentials` and `redshift`.
* Don't forget to start your Redshift cluster via the AWS console.
* After completing these steps, run your DAG to ensure all tasks are successfully executed.

## Getting Started with the Project
This project includes   
* The **DAG Script**  with task dependencies found in [final_project.py](dags%2Ffinal_project.py).
* The **operators** folder with operator here [operators](plugins%2Foperators).
* A **helper class** for SQL transformations here [helpers](plugins%2Fhelpers).


## DAG Configuration
Below is the `default parameters` user
```json
 'owner': 'Philip',
 'start_date': pendulum.datetime(2018, 11, 1, 0, 0, 0),
 'depends_on_past': False,
 'retries': 3,
 'retry_delay': timedelta(minutes=5),
 'catchup': False,
 'email_on_retry': False
```


## Developing Operators
I built four operators for staging data, transforming data, and performing data quality checks.

### Stage Operator
Found in [stage_redshift.py](plugins%2Foperators%2Fstage_redshift.py)  
This loads any JSON-formatted files from S3 to Amazon Redshift using the stage operator. The operator create and run a SQL COPY statement based on provided parameters, distinguishing between JSON files. It also support loading timestamped files from S3 based on execution time for backfills.

### Fact and Dimension Operators
Found in [load_fact.py](plugins%2Foperators%2Fload_fact.py) and [load_dimension.py](plugins%2Foperators%2Fload_dimension.py)  
This performs data transformations. These operator take a SQL statement, target database, and optional target table as input.
For dimension loads, it implement the truncate-insert pattern, allowing for switching between insert modes.

### Data Quality Operator
Found in [data_quality.py](plugins%2Foperators%2Fdata_quality.py)  
This creates the data quality operator to run checks on the data using SQL-based test cases and expected results.

## Result
Below is the expected DAG graph when you trigger the `final_project` dag
![Screenshot 001.png](assets%2FScreenshot%20001.png)
## Authors

## License