import socket
import os
import pandas as pd

# CONSTANTS
METRICS_CSV_PATH = './../../lab-sysadmin-data/metrics.csv'

# BASH

def execute_bash_command(cmd) -> str:
    """
    Execute a bash command.
    """

    # Execute the command
    stream = os.popen(cmd)

    # Get the output
    output = stream.read().strip()

    return output

# METRICS

def get_num_processes() -> dict:
    """
    Get the number of processes running on the instance.

        - Processes
    """

    # Get the number of processes
    cmd = """ps axu | wc -l"""
    processes = execute_bash_command(cmd) # 7

    metrics = {
        "Processes": str(processes),
    }

    return metrics

def get_cpu_utilization() -> dict:
    """
    Get the CPU utilization of the instance.

        - CPUUtilization
    """

    # Get the CPU utilization
    cmd = """grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}'"""
    cpu_utilization = execute_bash_command(cmd) # 16.457%

    metrics = {
        "CPUUtilization": cpu_utilization,
    }

    return metrics

def get_memory_utilization() -> dict:
    """
    Get the Memory utilization of the instance.

        - MemTotal
        - MemFree
        - MemAvailable
        - Cached
        - SwapCached
        - SwapTotal
        - SwapFree
    """

    # Get the Swap memory
    cmd = """egrep 'Mem|Cache|Swap' /proc/meminfo"""

    # Returns
    # MemTotal:         988680 kB
    # ......
    # SwapFree:              0 kB

    memories = execute_bash_command(cmd)

    # Split into memory datas
    memories_datas = memories.split('\n')

    # Initialize the metrics
    metrics = {}

    # Loop through the swap types
    for data in memories_datas:

        # Split the memory type
        infos = data.split(':')

        # Get the memory data
        name = infos[0].strip()
        value = infos[1].strip() # value: 0 kB

        # Convert to MB
        value = int(value.split(' ')[0]) / 1024 # value: 0
        value = f'{value}MB' # value: 0MB

        # Add to metrics
        metrics[name] = value

    return metrics

def get_disk_utilization() -> dict:

    # Get the disk utilization
    cmd = """df -h --total | sed -n '1p;$p'"""

    # Return
    # Filesystem      Size  Used Avail Use% Mounted on
    # total            10G  2.2G  7.9G  22% -

    disk_utilization = execute_bash_command(cmd) 

    # Split into disk datas
    disk_datas = disk_utilization.split('\n')

    # Disk metric names
    names = [data.strip() for data in disk_datas[0].split()]
    values = [data.strip() for data in disk_datas[1].split()]

    # Initialize the metrics
    metrics = {}

    # Get Size
    id_ = names.index('Size')
    metrics['DiskSize'] = values[id_]

    # Get Available
    id_ = names.index('Avail')
    metrics['DiskAvailable'] = values[id_]

    # Get Used
    id_ = names.index('Used')
    metrics['DiskUsed'] = values[id_]

    # Get Use%
    id_ = names.index('Use%')
    metrics['DiskUse%'] = values[id_]

    return metrics

def get_timestamp() -> dict:
    """
    Get the timestamp of the instance.

        - Timestamp
    """

    # Get the date
    cmd = """date +'%Y-%m-%d %H:%M:%S UTC'"""
    timestamp = execute_bash_command(cmd) # 2018-01-01 00:00:00 UTC

    metrics = {
        "Timestamp": timestamp,
    }

    return metrics

def update_metrics():
    """
    This method queries all metrics and update the local csv data
    """

    # Bool to check if the metrics csv file exists
    metrics_csv_exists = os.path.isfile(METRICS_CSV_PATH)

    # Load the metrics csv (if exists)
    if metrics_csv_exists:
        metrics_df = pd.read_csv(METRICS_CSV_PATH)

    # Get the metrics
    metrics_data = get_metrics()

    # Get the metric names and values
    metric_names = metrics_data['MetricNames']
    metric_values = metrics_data['MetricValues']

    # Add the metrics to the dataframe
    if not metrics_csv_exists:
        metrics_df = pd.DataFrame(columns=metric_names)
    
    # Double check df col order
    metrics_df = metrics_df[metric_names]
    
    # Add the metric values
    metrics_df.loc[len(metrics_df)] = metric_values

    # Save the metrics csv
    metrics_df.to_csv(METRICS_CSV_PATH, index=False)

def get_metrics() -> dict:
    """
    Return the instance metrics
    """

    # Get all metrics
    metrics = {}

    # Get the number of processes
    metrics.update(get_num_processes())

    # Get the CPU utilization
    metrics.update(get_cpu_utilization())

    # Get the Memory utilization
    metrics.update(get_memory_utilization())

    # Get the Disk utilization
    metrics.update(get_disk_utilization())

    # Get the timestamp
    metrics.update(get_timestamp())

    # Get the private IP
    metrics.update(get_private_ip())

    # Set metric names
    metric_names = sorted(list(metrics.keys()))

    # Set metric values
    metric_values = [metrics[name] for name in metric_names]

    return {
        "MetricNames": metric_names,
        "MetricValues": metric_values,
    }


def prepare_metrics() -> list:
    """
    This method returns data of ec2 metrics
    """

    # Get csv metrics
    metrics_df = pd.read_csv(METRICS_CSV_PATH)

    # Set names
    data = [
        list(metrics_df.columns)
    ]

    # Get the metrics
    for _, row in metrics_df.iterrows():
        data.append(list(row))

    return data

def get_private_ip() -> dict:
    """
    Get the private IP address of the instance.
    """

    # Get the private IP (from hostname)
    hostname = str(socket.gethostname()) # hostname: ip-10-0-0-0
    private_ip = '.'.join(hostname.split('-')[1:]) # ip: 10.0.0.0

    return {
        "PrivateIP": private_ip,
    }

# METRICS MANAGEMENT
