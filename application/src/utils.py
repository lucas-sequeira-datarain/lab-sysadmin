import socket
import os


def execute_bash_command(cmd) -> str:
    """
    Execute a bash command.
    """

    # Execute the command
    stream = os.popen(cmd)

    # Get the output
    output = stream.read().strip()

    return output

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
    memories = execute_bash_command(cmd) # SwapCached:            0 kB\nSwapTotal:             0 kB\nSwapFree:              0 kB

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
        value = value.replace(' ', '') # value: 0kB

        # Add to metrics
        metrics[name] = value

    return metrics

def get_disk_utilization() -> dict:

    # Get the disk utilization
    cmd = """df -T -h /dev/root"""

    # Return
    # Filesystem     Type  Size  Used Avail Use% Mounted on
    # /dev/root      ext4  7.7G  2.5G  5.3G  32% /

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

def get_ec2_metrics():
    """
    This method returns data of ec2 metrics
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

    data = [
        metric_names,
        metric_values,
    ]

    return data

def get_private_ip():
    """
    Get the private IP address of the instance.
    """

    # Get the private IP (from hostname)
    hostname = str(socket.gethostname()) # hostname: ip-10-0-0-0
    private_ip = '.'.join(hostname.split('-')[1:]) # ip: 10.0.0.0

    return {
        "PrivateIP": private_ip,
    }
