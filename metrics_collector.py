import json
from os.path import exists
from os import makedirs

from tqdm import tqdm

from prom_queries import *
from metrics import (
    generate_metrics_json,
    aggregate_metric_by_nodes,
    export_aggregated_metrics_csv
)

DATASETS_PATH = "metrics_datasets/"

if __name__ == "__main__":

    executions_logs = {}
    with open('raw_logs_13-09-21-00:03:09.json', 'r') as raw_logfile:
        executions_logs = json.load(raw_logfile)

    queries = {
        "cpu_usage_percentage": Q_NODES_CPU_USAGE_PERCENTAGE,
        "cpu_iowait_percentage": Q_NODES_CPU_IOWAIT_PERCENTAGE,
        "network_recv_bits": Q_NODES_NETWORK_TRAFIC_RECV,
        "network_trans_bits": Q_NODES_NETWORK_TRAFIC_TRANS,
        "io_sda_written_bytes": Q_NODES_IO_WRITE,
        "io_sda_readed_bytes": Q_NODES_IO_READ,
        "ram_usage_bytes": Q_NODES_RAM_USAGE,
        "swap_usage_bytes": Q_NODES_SWAP_USAGE,
        "usb_storage_used_space_bytes": Q_NODES_STORAGE_USED_SPACE
    }

    metrics_data = generate_metrics_json(executions_logs, queries, "ycsb_execution_metrics.json")

    if not exists(DATASETS_PATH):
        makedirs(DATASETS_PATH)

    for query_name in tqdm(queries.keys(), desc="Generating metrics datasets"):
        aggregated_metric = aggregate_metric_by_nodes(metrics_data, query_name)
        export_aggregated_metrics_csv(aggregated_metric, f"{DATASETS_PATH}{query_name}.csv")

    print("FINISHED!")
