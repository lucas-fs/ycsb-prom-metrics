from constants import IRATE_RANGE

q_cpu_usage = (
    'clamp_min(100 - (avg by (instance)(irate(node_cpu_seconds_total{mode="idle", job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])) * 100), 0)'
)

q_network_trafic_recv_query = (
    'irate(node_network_receive_bytes_total{device="eth0",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])*8'
)

q_network_trafic_trans_query = (
    'irate(node_network_transmit_bytes_total{device="eth0",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])*8'
)

q_io_write = (
    'irate(node_disk_written_bytes_total{'
    'device="sda",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])')

# FIXME: Replace written metric by read metric!
q_io_read = (
    'irate(node_disk_written_bytes_total{device="sda",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])'
)

q_nodes_swap_usage = (
    '(node_memory_SwapTotal_bytes{job=~"rpi3.*"} - node_memory_SwapFree_bytes{job=~"rpi3.*"})'
)

q_nodes_ram_usage = (
    'node_memory_MemTotal_bytes{job=~"rpi3.*"} - node_memory_MemFree_bytes{job=~"rpi3.*"} - '
    '(node_memory_Cached_bytes{job=~"rpi3.*"} + node_memory_Buffers_bytes{job=~"rpi3.*"})'
)
