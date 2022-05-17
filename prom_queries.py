from constants import IRATE_RANGE

Q_CPU_USAGE = (
    'clamp_min(100 - (avg by (instance)(irate(node_cpu_seconds_total{mode="idle", job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])) * 100), 0)'
)

Q_NETWORK_TRAFIC_RECV_QUERY = (
    'irate(node_network_receive_bytes_total{device="eth0",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])*8'
)

Q_NETWORK_TRAFIC_TRANS_QUERY = (
    'irate(node_network_transmit_bytes_total{device="eth0",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])*8'
)

Q_IO_WRITE = (
    'irate(node_disk_written_bytes_total{'
    'device="sda",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])')

# FIXME: Replace written metric by read metric!
Q_IO_READ = (
    'irate(node_disk_written_bytes_total{device="sda",job=~"rpi3.*"}'
    f'[{IRATE_RANGE}])'
)

Q_NODES_SWAP_USAGE = (
    '(node_memory_SwapTotal_bytes{job=~"rpi3.*"} - node_memory_SwapFree_bytes{job=~"rpi3.*"})'
)

Q_NODES_RAM_USAGE = (
    'node_memory_MemTotal_bytes{job=~"rpi3.*"} - node_memory_MemFree_bytes{job=~"rpi3.*"} - '
    '(node_memory_Cached_bytes{job=~"rpi3.*"} + node_memory_Buffers_bytes{job=~"rpi3.*"})'
)
