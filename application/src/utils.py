import socket

def get_ec2_metrics():
    """
    This method returns data of ec2 metrics
    """

    data = [
        [
            "Timestamp", "CPUUtilization", "RAMMemory", "SWAP", "Disk", "RunningTasksAmount"
        ],
        [
            "2018-01-01T00:00:00", "5.0", "1.5", "5.5", "3.6", "3.6"
        ],
        [
            "2018-01-01T00:05:00", "5.8", "2.5", "3.6", "3.4", "3.6"
        ],
        [
            "2018-01-01T00:10:00", "5.7", "2.5", "2.5", "3.6", "6.8"
        ],
    ]

    return data

def get_private_ip():
    """
    Get the private IP address of the instance.
    """

    # Get the private IP (from hostname)
    hostname = str(socket.gethostname()) # hostname: ip-10-0-0-0
    private_ip = '.'.join(hostname.split('-')[1:]) # ip: 10.0.0.0

    return private_ip
