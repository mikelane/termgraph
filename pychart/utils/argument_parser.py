import argparse

import settings
from settings import Colors


def get_cli_args():
    """Parse and return the arguments."""
    parser = argparse.ArgumentParser(
        description='draw basic graphs on terminal')
    parser.add_argument(
        'filename',
        nargs='?',
        default="-",
        help='data file name (comma or space separated). Defaults to stdin.')
    parser.add_argument(
        '--title',
        help='Title of graph'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=50,
        help='width of graph in characters default:50'
    )
    parser.add_argument(
        '--format',
        default='{:<5.2f}',
        help='format specifier to use.'
    )
    parser.add_argument(
        '--suffix',
        default='',
        help='string to add as a suffix to all data points.'
    )
    parser.add_argument(
        '--no-labels',
        action='store_true',
        help='Do not print the label column'
    )
    parser.add_argument(
        '--colors',
        nargs='*',
        choices=list(Colors.__members__.keys()),
        help='Chart bar color(s)'
    )
    parser.add_argument(
        '--vertical',
        action='store_true',
        help='Vertical graph'
    )
    parser.add_argument(
        '--stacked',
        action='store_true',
        help='Stacked bar graph'
    )
    parser.add_argument(
        '--different-scale',
        action='store_true',
        help='Categories have different scales.'
    )
    parser.add_argument(
        '--calendar',
        action='store_true',
        help='Calendar Heatmap chart'
    )
    parser.add_argument(
        '--start-dt',
        help='Start date for Calendar chart'
    )
    parser.add_argument(
        '--tick',
        default=settings.tick,
        help='Custom tick mark, emoji approved'
    )
    parser.add_argument(
        '--small-tick',
        default=settings.small_tick,
        help='Custom small tick mark'
    )
    parser.add_argument(
        '--delim',
        default=settings.delimiter,
        help='Custom delimiter, default , or space'
    )
    parser.add_argument(
        '-v', '--verbosity',
        action='count',
        default=2,
        help='Increase output verbosity'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Display version and exit'
    )

    return parser.parse_args()
