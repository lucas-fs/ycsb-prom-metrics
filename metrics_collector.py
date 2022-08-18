import json
from os.path import exists
from os import makedirs

from tqdm import tqdm

from prom_queries import *
from metrics import (
    export_all_metric_samples_dataset,
    generate_metrics_json,
    aggregate_metric_by_nodes,
    export_aggregated_metrics_csv
)

DATASETS_PATH = "metrics_datasets/"

if __name__ == "__main__":

    executions_logs = {}
    with open('raw_logs_merged.json', 'r') as raw_logfile:
        print(f"Reading values from the raw_logs_merged.json file...")
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

    # metrics_data = generate_metrics_json(executions_logs, queries, "ycsb_execution_metrics.json")
    metrics_data = {}
    with open('ycsb_execution_metrics.json', 'r') as raw_logfile:
        print(f"Reading values from the ycsb_execution_metrics.json file...")
        metrics_data = json.load(raw_logfile)

    if not exists(DATASETS_PATH):
        makedirs(DATASETS_PATH)

    nodes_count = 0
    with open('nodes.json', 'r') as nodes_file:
        nodes = json.load(nodes_file)
        nodes_count = len(nodes.keys())

    for query_name in tqdm(queries.keys(), desc="Generating agregated metrics datasets"):
        aggregated_metric = aggregate_metric_by_nodes(metrics_data, query_name)
        dataset_columns = list(aggregated_metric[0].keys())
        start_columns = dataset_columns[:-nodes_count]
        end_columns = sorted(dataset_columns[-nodes_count:])
        dataset_column_order = [*start_columns, *end_columns]
        export_aggregated_metrics_csv(
            aggregated_metric, f"{DATASETS_PATH}{query_name}.csv", dataset_column_order
        )

    for query_name in tqdm(queries.keys(), desc="Generating all metrics samples datasets"):
        dataset_column_order = [
            "database", "replication_factor", "recordcount", "workload", "execution", "start", "end",
            "duration", "metric_sample_index", "rpi3_01", "rpi3_02", "rpi3_03", "rpi3_04", "rpi3_05",
            "rpi3_06", "rpi3_07", "rpi3_08", "rpi3_09", "rpi3_10", "rpi3_11", "rpi3_12", "rpi3_13",
            "rpi3_14", "rpi3_15"
        ]

        export_all_metric_samples_dataset(
            metrics_data, query_name, f"{DATASETS_PATH}{query_name}-raw-data.csv", dataset_column_order
        )

    print("FINISHED!")
