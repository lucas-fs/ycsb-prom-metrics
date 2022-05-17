import requests
import locale
import pytz
import time
import json

from statistics import mean
from collections import defaultdict
from datetime import datetime
from numpy import nan as NaN
from tqdm import tqdm
import pandas as pd

from constants import (
    STEP_RESOLUTION,
    WINDOW_STEPS,
    PROMETHEUS_URL
)


def to_unix_timestamp(ascii_date):
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    local_timezone = pytz.timezone('America/Sao_Paulo')

    date_format = "%a %b %d %H:%M:%S %Y"

    local_date = datetime.strptime(ascii_date.replace(" -03", ""), date_format)

    local_date = local_timezone.localize(local_date)
    utc_date = local_date.astimezone(pytz.UTC)

    return time.mktime(utc_date.timetuple())


def to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp)


def prom_get_range_metrics(query, start_time, end_time, nodes, step_resolution, window=0):

    api_endpoint_url = PROMETHEUS_URL + "/api/v1/query_range"
    request_params = {
        'query': query,
        'start': start_time - window,
        'end': end_time + window,
        'step': step_resolution
    }
    response = requests.get(api_endpoint_url, params=request_params)
    results = response.json()

    range_metrics = {}
    for metric in results['data']['result']:
        instance = str(metric['metric']['instance'])
        range_metrics[nodes[instance]] = []

        for value in metric['values']:
            usage_value = float("{:.2f}".format(float(value[1])))
            range_metrics[nodes[instance]].append(usage_value)

    return range_metrics


def align_lists(executions):
    sizes = set()
    for ex in list(executions):
        sizes.add(len(executions[ex]))

    max_size = max(sizes)
    for ex in list(executions):
        nan_sublist = [NaN]*(max_size-len(executions[ex]))
        slice_pos = len(executions[ex]) - WINDOW_STEPS
        executions[ex][slice_pos:slice_pos] = nan_sublist

    return executions


def trunc(original_list, trunc_values):
    if trunc_values:
        original_l = [str(x) for x in original_list]
        trunc_l = [str(x) for x in trunc_values]
        return [x for x in original_l if x not in trunc_l]
    else:
        return original_list


def aggregate_metric_by_nodes(metrics, metric_to_aggregate, trunc_values=None):
    aggregated_metrics = []

    for database in list(metrics):
        for replication_f in list(metrics[database]):
            for recordcount in list(metrics[database][replication_f]):
                for workload in list(metrics[database][replication_f][recordcount]):
                    for execution in trunc(list(metrics[database][replication_f][recordcount][workload]), trunc_values):
                        execution_metrics = metrics[database][replication_f][recordcount][workload][execution]
                        data_row = {
                            "database": str(database),
                            "replication_factor": str(replication_f),
                            "recordcount": str(recordcount),
                            "workload": str(workload),
                            "execution": str(execution),
                            "start": str(to_datetime(execution_metrics["start"])),
                            "end": str(to_datetime(execution_metrics["end"])),
                            "duration": execution_metrics["duration"]
                        }

                        for node, exe_metrics in execution_metrics[str(metric_to_aggregate)].items():
                            data_row[node] = mean(exe_metrics)

                        aggregated_metrics.append(data_row)
                        
    return aggregated_metrics


def generate_metrics_json(execution_logs, queries, filename):
    metrics = defaultdict(     # databases
        lambda: defaultdict(       # replication factors
            lambda: defaultdict(       # recordcounts
                lambda: defaultdict(       # workloads
                    lambda: defaultdict(       # executions
                        dict                       # execution metrics
                    )
                )
            )
        )
    )

    nodes = {}
    with open('nodes.json', 'r') as nodes_file:
        nodes = json.load(nodes_file)

    for log in tqdm(execution_logs, desc="Collecting Prometheus metrics"):
        execution_metrics = {}

        start = to_unix_timestamp(str(log.get("start")))
        end = to_unix_timestamp(str(log.get("end")))
        window = WINDOW_STEPS * STEP_RESOLUTION

        execution_metrics = {
            'start': start,
            'end': end,
            'duration': (end-start),
            'step': STEP_RESOLUTION
        }

        for query_name, query in queries.items():
            execution_metrics[query_name] = prom_get_range_metrics(
                query=query,
                start_time=start,
                end_time=end,
                nodes=nodes,
                step_resolution=STEP_RESOLUTION,
                window=window
            )

        database = str(log.get("database"))
        replication_factor = str(log.get("replication_factor"))
        recordcount = str(log.get("recordcount"))
        workload = str(log.get("workload"))
        execution = str(log.get("execution"))

        metrics[database][replication_factor][recordcount][workload][execution] = execution_metrics

    with open(str(filename), 'w') as metrics_file:
        json.dump(metrics, metrics_file, indent=4, ensure_ascii=False)

    return metrics
