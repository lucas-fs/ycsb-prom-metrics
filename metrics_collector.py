import json

from metrics import generate_metrics_json
from prom_queries import *

if __name__ == "__main__":

    executions_logs = {}
    with open('raw_logs_13-09-21-00:03:09.json', 'r') as raw_logfile:
        executions_logs = json.load(raw_logfile)

    queries = {
        'cpu_usage': q_cpu_usage,
        'network_recv': q_network_trafic_recv_query,
        'network_trans': q_network_trafic_trans_query,
        'io_written': q_io_write,
        'io_read': q_io_read,
        'ram_usage': q_nodes_ram_usage,
        'swap_usage': q_nodes_swap_usage
    }

    metrics_data = generate_metrics_json(executions_logs, queries, "ycsb_execution_metrics.json")

    print("DONE!")
