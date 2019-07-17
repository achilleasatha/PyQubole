# A simple example of how to use the connector

from pyqubole.connector import QuboleConnector

if __name__ == "__main__":
    con = QuboleConnector(api_token='api_token')

    query = r"""select * from table""" # direct query input
    # query = open('query.sql').read() # import from local file

    # If job_id is None query will be executed if job_id is given the output will be retrieved if job is complete
    data = con.query_data(sql_query=query, job_id=None, engine='Hive', cluster='Hive_cluster_name')
