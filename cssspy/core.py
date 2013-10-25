import sys
from .cli import get_args


def main():
    run_scrapy(get_args())
