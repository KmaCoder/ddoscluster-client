import argparse

from src.config import DEFAULT_THREADS


def get_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Client name', type=str, required=True)
    parser.add_argument('--threads', help='Threads count', type=int, default=DEFAULT_THREADS)

    return parser.parse_args()
