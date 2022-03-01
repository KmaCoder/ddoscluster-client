import argparse

from src.config import DEFAULT_THREADS_PER_PROCESS


def get_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='client name', type=str, required=True)
    parser.add_argument('--threads', help='connection threads count per process', type=int, default=DEFAULT_THREADS_PER_PROCESS)

    return parser.parse_args()
