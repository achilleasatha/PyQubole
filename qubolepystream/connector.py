import os
from qds_sdk.qubole import Qubole
from qds_sdk.commands import HiveCommand, PrestoCommand, SparkCommand
from io import BytesIO
import re
import time
import pandas as pd
import json
import warnings


class QuboleConnector:
    def __init__(self, api_token=None):
        self._check_qubole_api_token_is_assigned(api_token=api_token)
        Qubole.configure(api_token=api_token)
        print('Connected to Qubole')
        self.old_std_out = []
        self.status = None

    def _check_qubole_api_token_is_assigned(self, api_token=None):
        if api_token is None:
            if os.environ.get('QUBOLE_API_TOKEN') is None:
                warnings.warn("Qubole API Token is not set => os.environ['QUBOLE_API_TOKEN']")
                api_token = os.environ['QUBOLE_API_TOKEN'] = input('Input Qubole API Token (as string): ')
            else:
                api_token = os.environ.get('QUBOLE_API_TOKEN')
        return api_token

    def query_data(self, sql_query, job_id=None, engine=None, cluster=None, verbose=False, **kwargs):
        if sql_query is None or sql_query == '':
            raise RuntimeError('Query is empty')
        if job_id:
            cmd = self.get_completed_job(job_id=job_id)
        elif engine == 'Hive':
            cmd = self.read_data_from_hive(sql_query, cluster, verbose, **kwargs)
        elif engine == 'Presto':
            cmd = self.read_data_from_presto(sql_query, cluster, verbose, **kwargs)
        elif engine == 'Spark':
            cmd = self.run_spark_job(sql_query, cluster, verbose, **kwargs)
            return print('Command successfully executed, command_id=%s' % cmd.attributes.get('id'))
        else:
            raise Exception('Both cluster and engine need to be specified!')
        fh = BytesIO()
        cmd.get_results(fh, inline=False, fetch=True, delim=chr(9), arguments=['true'])
        fh.seek(0)
        qlog = json.loads(cmd.attributes['qlog'])
        cols = qlog['QBOL-QUERY-SCHEMA'][list(qlog['QBOL-QUERY-SCHEMA'].keys())[0]]
        col_names = [re.sub(r'.+\.', '', col['ColumnName']) for col in cols]  # regex formats names for aliased tables
        return pd.read_csv(fh, delimiter=chr(9), names=col_names, na_values='\\N')

    def read_data_from_hive(self, query, cluster, verbose=False, **kwargs):
        print('Running Hive query')
        cmd = HiveCommand.create(query=query, print_logs_live=True, label=cluster, **kwargs)
        while cmd.attributes.get('status', None) != 'done':
            if verbose:
                cmd = self._get_logs(cmd)
            else:
                cmd = self._get_status(cmd)
        return cmd

    def read_data_from_presto(self, query, cluster, verbose=False, **kwargs):
        print('Running Presto query')
        cmd = PrestoCommand.create(query=query, label=cluster, **kwargs)
        while cmd.attributes.get('status', None) != 'done':
            if verbose:
                cmd = self._get_logs(cmd)
            else:
                cmd = self._get_status(cmd)
        return cmd

    def run_spark_job(self, query, cluster, verbose=False, **kwargs):
        print('Running Spark job')
        cmd = SparkCommand.create(query=query, label=cluster, **kwargs)
        while cmd.attributes.get('status', None) != 'done':
            if verbose:
                cmd = self._get_logs(cmd)
            else:
                cmd = self._get_status(cmd)
        return cmd

    def _get_logs(self, cmd):
        new_std_out = (cmd.get_log_partial()[0]).split('\n')
        for line in new_std_out[len(self.old_std_out):]:
            print(line)
        cmd = HiveCommand.find(cmd.id)
        self.old_std_out = new_std_out
        time.sleep(5)
        if cmd.attributes['status'] == 'error':
            raise RuntimeError('Job Failed')
        if cmd.attributes['status'] == 'cancelled':
            raise RuntimeError('Job Cancelled')
        return cmd

    def _get_status(self, cmd):
        old_status = self.status
        self.status = cmd.attributes['status']
        if self.status == 'error':
            raise RuntimeError('Job Failed')
        if self.status == 'cancelled':
            raise RuntimeError('Job Cancelled')
        if old_status != self.status:
            print(self.status)
        cmd = cmd.find(cmd.attributes['id'])
        return cmd

    @staticmethod
    def get_completed_job(job_id):
        cmd = HiveCommand()
        cmd = cmd.find(job_id)
        print('Retrieving job:', job_id)
        if cmd.attributes.get('status', None) != 'done':
            raise ValueError('Job not yet completed')
        print('Job data successfully retrieved from Qubole')
        return cmd
