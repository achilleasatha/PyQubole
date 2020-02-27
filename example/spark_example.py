from qubolepystream.connector import QuboleConnector


if __name__ == "__main__":
    ''' A simple example of how to use the connector to run a Spark job.'''
    con = QuboleConnector(api_token='api_token')

    prog = '''
    import sys
    from random import random
    from operator import add

    from pyspark import SparkContext


    if __name__ == "__main__":
        """
            Usage: pi [partitions]
        """
        sc = SparkContext(appName="PythonPi")
        partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
        n = 100000 * partitions

        def f(_):
            x = random() * 2 - 1
            y = random() * 2 - 1
            return 1 if x ** 2 + y ** 2 < 1 else 0

        count = sc.parallelize(xrange(1, n + 1), partitions).map(f).reduce(add)
        print "Pi is roughly %f" % (4.0 * count / n)

        sc.stop()
    '''

    con.query_data(sql_query=None, job_id=None, engine='Spark', cluster='Spark_Cluster',
                   program=prog, language='python', verbose=False)
    # languages supported ['python', 'scala', 'R']