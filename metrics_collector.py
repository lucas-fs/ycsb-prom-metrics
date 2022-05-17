import json

from metrics import generate_metrics_json
from prom_queries import *

if __name__ == "__main__":

    executions_logs = {}
    with open('raw_logs_13-09-21-00:03:09.json', 'r') as raw_logfile:
        executions_logs = json.load(raw_logfile)

    queries = {
        'cpu_usage': Q_CPU_USAGE,
        'network_recv': Q_NETWORK_TRAFIC_RECV_QUERY,
        'network_trans': Q_NETWORK_TRAFIC_TRANS_QUERY,
        'io_written': Q_IO_WRITE,
        'io_read': Q_IO_READ,
        'ram_usage': Q_NODES_RAM_USAGE,
        'swap_usage': Q_NODES_SWAP_USAGE
    }

    metrics_data = generate_metrics_json(executions_logs, queries, "ycsb_execution_metrics.json")

    print("DONE!")
