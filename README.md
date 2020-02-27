# PyQubole
A watered down version of Qubole's Python connector providing a much simpler API to interact with for running streaming queries or submitting a job and rerieving its output at a later time (sync or async). Allowing for easy use in notebooks or integration in projects without much overhead. Based on Qubole QDS-SDK-Py https://github.com/qubole/qds-sdk-py

## Installtion
### From PyPI
The library is available on [PyPI - PyQubole](https://pypi.org/project/qubolepystream/).

`$ pip install qubolepystream`

### From Source
•Get source code: SSH `git@github.com:achilleasatha/PyQubole.git` or HTTPS `https://github.com/achilleasatha/PyQubole.git` 


•Install by running `python setup.py install` 

## API
You can find an example application in [example/main.py](https://github.com/achilleasatha/PyQubole/blob/master/example/main.py) including a Spark command example [example/spark_example.py](https://github.com/achilleasatha/PyQubole/blob/master/example/spark_example.py).

More info on running Spark commands: [Qubole docs - Submit a Spark command](https://docs.qubole.com/en/latest/rest-api/command_api/submit-a-spark-command.html)

An example application needs to do:
  1. Import the lib `from qubolepystream.connector import QuboleConnector`
  2. Set the api_token and instantiate the connection
  `con = QuboleConnector(api_token='api_token')`
  3. Use the query data method to run a job, specifying the input query, engine and cluster (or just job_id):
  `data = con.query_data(sql_query=query, job_id=None, engine='Hive', cluster='Hive_cluster_name', verbose=False)`
  
  Note:
  
  a) Query can be passed as a raw string `query = r"""select * from table"""` or from a file: `query = open('query.sql').read()`
  
  b) If `job_id = None` the query will be executed on the engine specified ('Hive', 'Presto' or 'Spark'')
    
  c) If `job_id = '123456'` then the results of the job will be retrieved (if job status is done)
    
  d) You can use the optional method `verbose = True / False` to get streaming logs output or only status updates
    
