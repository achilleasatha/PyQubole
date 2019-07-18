from pyqubole.connector import QuboleConnector


if __name__ == "__main__":
    ''' A simple example of how to use the connector '''
    con = QuboleConnector(api_token='api_token')

    query = r"""select * from table"""
    # query = open('query.sql').read() # import from local file

    # Use job_id to retrieve job and verbose=True for streaming output
    data = con.query_data(sql_query=query, job_id=None, engine='Hive', cluster='Hive_cluster_name', verbose=False)
