import argparse

from config import DEFAULT_THREADS


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Client name', type=str, required=True)
    parser.add_argument('--threads', help='Threads count', type=int, default=DEFAULT_THREADS)

    parser.print_help()
    return parser.parse_args()
