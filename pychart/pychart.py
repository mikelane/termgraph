#!/usr/bin/env python3
# coding=utf-8
"""This module allows drawing basic graphs in the terminal."""

# pychart.py - draw basic graphs on terminal
# https://github.com/mikelane/termgraph

from itertools import cycle, islice
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

import pandas as pd

import settings
from settings import Colors


class Chart:
    def __init__(self, colors: Optional[Iterable[settings.Colors]] = None, data: str = 'No Data',
                 delimiter: str = settings.delimiter, different_scale: bool = False,
                 filename: Union[str, Path, None] = None, no_labels: bool = False,
                 small_tick: str = settings.small_tick, suffix: str = '', tick: str = settings.tick,
                 title: Optional[str] = None, width: int = 50):
        self.colors = colors if colors else []
        self.data: Union[str, Dict[str, dict]] = data
        self.delimiter = delimiter
        self.different_scale = different_scale
        self.filename = filename
        self.no_labels = no_labels
        self.small_tick = small_tick
        self.suffix = suffix
        self.tick = tick
        self.title = title
        self.width = width

        self.headers: List[str] = []
        self.output_string: str = 'No Data'
        self.scaled_data: Union[str, Dict[str, dict]] = 'No Data'

        self.__column2color: Optional[Dict[str, settings.Colors]] = None
        self.__data_start_row_number: int = 0
        self.__dataframe: Optional[pd.DataFrame]
        self.__legend: Optional[str] = None
        self.__max_index_length: int = 0
        self.__num_categories: int = 0
        self.__output_rows: Optional[List[str]] = None
        self.__reset: Colors = Colors.reset.value
        self.__scaled_dataframe: Optional[pd.DataFrame] = None

        if self.filename:
            self._get_headers()
            self._read_data_from_file(self.filename)
            self._scale_data()
            self._parse_data()
            self._set_colors()
            if self.colors:
                self._build_legend()
            self._build_output_row_list()
            self.build_output_string()

    def __str__(self):
        return self.output_string

    def _build_legend(self):
        self.__legend = ' '.join(
            [f'{self.__column2color[column]}{self.tick} {column}' for column in self.headers] + [self.__reset])

    def _build_output_row_list(self):
        self.__output_rows = []
        for index, rows in self.scaled_data.items():
            for i, (column, number_of_blocks) in enumerate(rows.items()):
                self.__output_rows.append(
                    self._build_row(
                        index=index if i == 0 else '',
                        length=self.__max_index_length,
                        color=self.__column2color[column],
                        tick=self.tick if number_of_blocks > 0 else self.small_tick,
                        number_of_blocks=max(1, number_of_blocks),
                        data_value=self.data[index][column]
                    )
                )

    def _build_row(self, index: str, length: int, color: Colors, tick: str, number_of_blocks: int,
                   data_value: float) -> str:
        return f'{index:>{length}}: {color}{tick * number_of_blocks} {self.__reset}{float(data_value):0.5}'

    def _get_headers(self):
        with open(self.filename, 'r') as input_file:
            for row_number, line in enumerate(input_file):
                if line.startswith(settings.header_row_marker):
                    self.headers = line.replace(settings.header_row_marker, '').strip().split(self.delimiter)
                    self.__num_categories = len(self.headers)
                    self.__data_start_row_number += 1
                    break
                elif line.startswith(settings.comment_marker):
                    self.__data_start_row_number += 1

    @staticmethod
    def _get_max_label_length(labels):
        """Return the maximum length for the labels."""
        return len(max(labels, key=len))

    def _parse_data(self):
        self.data = self.__dataframe.to_dict('index')
        self.scaled_data = self.__scaled_dataframe.to_dict('index')

    def _read_data_from_file(self, filename: str):
        self.__dataframe = pd.read_csv(
            filename,
            header=None,
            names=self.headers if self.headers else None,
            delimiter=self.delimiter if self.delimiter != ' ' else None,
            delim_whitespace=False if self.delimiter != ' ' else True,
            comment=settings.comment_marker,
            index_col=0,
            skiprows=self.__data_start_row_number,
        )

        # While we're here, get the max printing length of the index values.
        self.__max_index_length = len(str(max(self.__dataframe.index, key=lambda idx: len(str(idx)))))

        # Also, if we didn't find any headers, let the dataframe set the header values
        if not self.headers:
            self.headers = list(self.__dataframe.columns)

    def _scale_data(self):
        """Normalize the data for the desired width"""
        # Offset to the right for negative values
        self.__scaled_dataframe = self.__dataframe - min(0, self.__dataframe.values.min())
        if self.__scaled_dataframe.values.max() > self.width:
            # Scale between 0.0 and 1.0
            self.__scaled_dataframe = self.__scaled_dataframe / self.__scaled_dataframe.values.max()
            # Scale between 0 and width (rounding and converting to int),
            self.__scaled_dataframe = (self.__scaled_dataframe * self.width).round().astype(int)

    def _set_colors(self):
        # Set color values to empty strings if no colors are set
        # Also set reset to empty string
        if not self.colors:
            self.__column2color = {column: '' for column in self.headers}
            self.__reset = ''
            return

        # If user doesn't give enough colors, cycle through the colors they do provide
        if len(self.colors) < self.__num_categories:
            self.colors = list(islice(cycle(self.colors), self.__num_categories))

        # If they give more colors, truncate the colors them
        self.colors = self.colors[:self.__num_categories]

        # replace the colors with the colorama colors:
        try:
            self.__column2color = {
                column: color
                for column, color
                in zip(self.headers,
                       [Colors[color].value for color in self.colors])
            }
        except KeyError:
            raise ValueError(f'Invalid color selection. Colors must be in {Colors.__members__.keys()}')

    def build_output_string(self, filename: Union[str, Path, None] = None) -> str:
        """Build the chart string given a data file. Also sets the internal
        state so you can call print() on an instance of a Chart object."""
        if filename:
            self._get_headers()
            self._read_data_from_file(filename)
            self._scale_data()
            self._parse_data()
            self._set_colors()
            if self.colors:
                self._build_legend()
            self._build_output_row_list()

        title = f'{self.title}\n\n' if self.title else ''
        legend = f'{self.__legend}\n\n' if self.__legend else ''
        output_rows = "\n".join(self.__output_rows)

        text = title \
               + legend \
               + output_rows

        self.output_string = text
        return text

# def vertically(value, num_blocks, val_min, color, args):
#     """Prepare the vertical graph.
#        The whole graph is printed through the print_vertical function."""
#     global maxi, value_list
#
#     value_list.append(str(value))
#
#     # In case the number of blocks at the end of the normalization is less
#     # than the default number, use the maxi variable to escape.
#     if maxi < num_blocks:
#         maxi = num_blocks
#
#     if num_blocks > 0:
#         vertical_list.append((TICK * num_blocks))
#     else:
#         vertical_list.append(SM_TICK)
#
#     # Zip_longest method in order to turn them vertically.
#     for row in zip_longest(*vertical_list, fillvalue='  '):
#         zipped_list.append(row)
#
#     counter, result_list = 0, []
#
#     # Combined with the maxi variable, escapes the appending method at
#     # the correct point or the default one (width).
#     for i in reversed(zipped_list):
#         result_list.append(i)
#         counter += 1
#
#         if maxi == args['width']:
#             if counter == (args['width']):
#                 break
#         else:
#             if counter == maxi:
#                 break
#
#     # Return a list of rows which will be used to print the result vertically.
#     return result_list
#
#
# def print_vertical(vertical_rows, labels, color, args):
#     """Print the whole vertical graph."""
#     if color:
#         sys.stdout.write(f'\033[{color}m')  # Start to write colorized.
#
#     for row in vertical_rows:
#         print(*row)
#
#     sys.stdout.write('\033[0m')  # End of printing colored
#
#     print("-" * len(row) + "Values" + "-" * len(row))
#     # Print Values
#     for value in zip_longest(*value_list, fillvalue=' '):
#         print("  ".join(value))
#
#     if args['no_labels'] == False:
#         print("-" * len(row) + "Labels" + "-" * len(row))
#         # Print Labels
#         for label in zip_longest(*labels, fillvalue=''):
#             print("  ".join(label))
#

# def calendar_heatmap(data, labels, args):
#     """Print a calendar heatmap."""
#     if args['color']:
#         colornum = Colors[args['color'][0]]
#     else:
#         colornum = Colors['blue']
#
#     dt_dict = {}
#     for i in range(len(labels)):
#         dt_dict[labels[i]] = data[i][0]
#
#     # get max value
#     max_val = float(max(data)[0])
#
#     tick_1 = "░"
#     tick_2 = "▒"
#     tick_3 = "▓"
#     tick_4 = "█"
#
#     if args['custom_tick']:
#         tick_1 = tick_2 = tick_3 = tick_4 = args['custom_tick']
#
#     # check if start day set, otherwise use one year ago
#     if args['start_dt']:
#         start_dt = datetime.strptime(args['start_dt'], '%Y-%m-%d')
#     else:
#         start = datetime.now()
#         start_dt = datetime(year=start.year - 1, month=start.month,
#                             day=start.day)
#
#     # modify start date to be a Monday, subtract weekday() from day
#     start_dt = start_dt - timedelta(start_dt.weekday())
#
#     # TODO: legend doesn't line up properly for all start dates/data
#     # top legend for months
#     sys.stdout.write("     ")
#     for month in range(13):
#         month_dt = datetime(year=start_dt.year, month=start_dt.month, day=1) + \
#                    timedelta(days=month * 31)
#         sys.stdout.write(month_dt.strftime("%b") + " ")
#         if args['custom_tick']:  # assume custom tick is emoji which is one wider
#             sys.stdout.write(" ")
#
#     sys.stdout.write('\n')
#
#     for day in range(7):
#         sys.stdout.write(calendar.day_abbr[day] + ': ')
#         for week in range(53):
#             day_ = start_dt + timedelta(days=day + week * 7)
#             day_str = day_.strftime("%Y-%m-%d")
#
#             if day_str in dt_dict:
#                 if dt_dict[day_str] > max_val * 0.75:
#                     tick = tick_4
#                 elif dt_dict[day_str] > max_val * 0.50:
#                     tick = tick_3
#                 elif dt_dict[day_str] > max_val * 0.25:
#                     tick = tick_2
#                 else:
#                     tick = tick_1
#             else:
#                 tick = ' '
#
#             if colornum:
#                 sys.stdout.write(f'\033[{colornum}m')
#
#             sys.stdout.write(tick)
#             if colornum:
#                 sys.stdout.write('\033[0m')
#
#         sys.stdout.write('\n')
#
#
