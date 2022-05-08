import json

from collections import defaultdict
from statistics import mean
import pandas as pd

from metrics import group_metrics_by_nodes
from constants import STEP_RESOLUTION, WINDOW_STEPS


def get_mean_cpu_usage(node_executions):
    means = defaultdict(lambda: defaultdict(dict))

    for rc in list(node_executions):
        for wk in list(node_executions[rc]):
            duration_mean = mean(node_executions[rc][wk]['durations'])
            duration_m = float("{:.3f}".format(duration_mean))
            cpu_means = {}
            for node in list(node_executions[rc][wk]['cpu_usage']):
                cpu_means[node] = node_executions[rc][wk]['cpu_usage'][node].mean(
                    axis='columns', skipna=True)

            df = pd.DataFrame(cpu_means)
            rows_df = len(df.index)
            trunc_rows = int((duration_m // STEP_RESOLUTION)+1)
            p1 = rows_df-(rows_df-trunc_rows-WINDOW_STEPS)
            p2 = rows_df - WINDOW_STEPS

            refactored_df = df.drop(df.index[p1:p2]).reset_index(drop=True)

            means[rc][wk]['duration_mean'] = duration_m
            means[rc][wk]['cpu_usages_mean'] = refactored_df

    return means


def export_cpu_usage_dataset(cpu_means, filename):
    for rc in list(cpu_means):
        for wk in list(cpu_means[rc]):
            cpu_means[rc][wk]['cpu_usages_mean']['workload'] = wk
            cpu_means[rc][wk]['cpu_usages_mean']['recordcount'] = rc

    data_frames = []
    for rc in list(cpu_means):
        for wk in list(cpu_means[rc]):
            data_frames.append(cpu_means[rc][wk]['cpu_usages_mean'])

    dataset = pd.concat(data_frames)
    dataset.to_csv(filename, index_label="tempo")


if __name__ == "__main__":

    with open('ycsb_execution_metrics.json', 'r') as logs_file:
        logs = json.load(logs_file)

    node_executions = group_metrics_by_nodes(logs, truncate=[1, 2, 3])
    cpu_mean_usage = get_mean_cpu_usage(node_executions)

    export_cpu_usage_dataset(cpu_mean_usage, 'dataset-cpu.csv')
    print("DONE!")
