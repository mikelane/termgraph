from pathlib import Path

import colorama

from .pychart import Chart
from pychart.utils.argument_parser import get_cli_args
from settings import logging

args = get_cli_args()

logger = logging.get_logger(__name__, args.verbosity)


def cli():
    logger.info(Path(__file__).cwd())
    """Main function."""
    colorama.init()


    if args.version:
        pass
        # print(f'pychart v{__version__}')
        # return

    if args.calendar:
        logger.error('The calendar is not yet implemented')
        # calendar_heatmap(data, labels, args)
    else:
        chart = Chart(
            colors=args.colors,
            delimiter=args.delim,
            filename=args.filename,
            no_labels=args.no_labels,
            small_tick=args.small_tick,
            suffix=args.suffix,
            tick=args.tick,
            title=args.title,
            width=args.width,
        )
        print(chart)
